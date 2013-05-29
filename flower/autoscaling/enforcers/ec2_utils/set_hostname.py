from fabric.api import sudo


def set_hostname(hostname):
    sudo('echo %s > /etc/hostname' % hostname)