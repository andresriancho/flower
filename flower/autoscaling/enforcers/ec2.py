import logging

from fabric.api import settings

from .base import BaseEnforcer
from .utils.spawn_ec2 import spawn_ec2_instance
from .utils.deploy_celery import deploy_celery
from .utils.set_hostname import set_hostname
from .utils.shutdown_instance import shutdown_instance


class Ec2Enforcer(BaseEnforcer):
    '''
    Make sure to set all the correct values before running flower.
    '''
    
    # TODO: This should be configured from the flower web UI 
    CONF = {
            'EC2_KEY': '',
            'EC2_SECRET': '',
            'EC2_AMI': '',
            'EC2_KEY_PAIR': '',
            'EC2_SECURITY_GROUP': '',
            'EC2_INSTANCE_TYPE': 't1.micro',
            'EC2_INSTANCE_NAME_TAG': 'Celery worker',
            
            # The user to use with SSH/Fabric to connect to the remote server
            # The ssh key to access the server needs to be added to your
            # SSH agent for this script to work. See ssh-add -l
            'EC2_INSTANCE_USER': 'ubuntu',
            }
    
    def spawn(self, number):
        '''
        :param number: The number of workers which will be spawned
        '''    
        logging.debug('Spawning %s new workers.' % number)
        
        for _ in xrange(number):
            instance = spawn_ec2_instance(self.CONF)
            
            host = '%s@%s' % (self.CONF['EC2_INSTANCE_USER'],
                              instance.public_dns_name)
            
            with settings(host_string=host, use_ssh_config=True):
                # IMPORTANT!
                #
                # Set the hostname to the public DNS name. This is required
                # since the hostname is used as the worker name in celery, and
                # this will allow me to shutdown servers based on the celery
                # worker name.
                set_hostname(instance.public_dns_name)
                
                # Install celery on the remote server, and start the daemon
                deploy_celery(instance)
    
    def kill(self, workers):
        '''
        :param workers: The names of the workers to be killed
        '''    
        logging.debug('Killing %s workers.' % len(workers))
        
        for worker_name in workers:
            # Read IMPORTANT comment above about the worker_name and why we can
            # use it here as the DNS name of the host
            host = '%s@%s' % (self.CONF['EC2_INSTANCE_USER'],
                              worker_name)
            
            with settings(host_string=host, use_ssh_config=True):
                shutdown_instance()
                