import time
import logging

import boto.ec2

from fabric.api import task, env


@task
def spawn_ec2_instance(conf):
    """
    Launches a new EC2 Instance with the specified configuration.
    
    :param conf: The configuration as defined in ec2.CONF.
    """
    logging.info("Creating new EC2 instance...")

    conn = boto.ec2.connect_to_region('us-west-1',
                                      aws_access_key_id=conf['EC2_KEY'],
                                      aws_secret_access_key=conf['EC2_SECRET'])

    all_images = conn.get_all_images(image_ids=[conf['EC2_AMI'],])

    assert len(all_images) == 1
    image = all_images[0]

    reservation = image.run(1, 1, key_name=env.conf['EC2_KEY_PAIR'],
                            security_groups=[env.conf['EC2_SECURITY_GROUP'],],
                            instance_type=env.conf['EC2_INSTANCE_TYPE'])
 
    instance = reservation.instances[0]

    while instance.state == u'pending':
        logging.info("Instance state: %s" % instance.state)
        time.sleep(10)
        instance.update()
 
    # Add a tag, just for identification
    conn.create_tags([instance.id], {"Name":env.conf['EC2_INSTANCE_NAME_TAG']})

    logging.info("New instance public DNS: %s" % instance.public_dns_name)
 
    return instance
