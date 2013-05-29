from fabric.api import task

from celerydeploy.worker import setup, start

from .wait_for_ssh import wait_for_ssh


@task
def deploy_celery(instance):
    """
    Use fabric to connect to a newly spawned instance and deploy celery and
    our application.
    
    :param instance: An instance object as returned by the boto library, this
                     holds the IP address, DNS name, etc.
    """
    wait_for_ssh(instance.public_dns_name)
    
    # This will work without any parameters since it is being run in a settings()
    # context manager which sets the host_string and the SSH credentials
    setup()
    start()
 
    return instance
