from fabric.api import sudo


def shutdown():
    sudo('shutdown now -h')