import socket
import time
import logging


def wait_for_ssh(host):
    # Wait until the SSH is actually up
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            s.connect((host, 22))
        except:
            logging.debug('Waiting for SSH to be ready to connect')
            time.sleep(2)
        else:
            break