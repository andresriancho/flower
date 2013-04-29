import logging

from .base import BaseEnforcer


class Ec2Enforcer(BaseEnforcer):
    
    def spawn(self, number):
        '''
        :param number: The number of workers which will be spawned
        '''    
        logging.debug('Spawning %s new workers.' % number)
    
    def kill(self, workers):
        '''
        :param workers: The names of the workers to be killed
        '''    
        logging.debug('Killing %s workers.' % workers)