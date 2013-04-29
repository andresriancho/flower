import logging

from settings import MIN_WORKERS, MAX_WORKERS
from flower.autoscaling.strategy import NaiveStrategy


class GenericAutoscaler(object):
    def __init__(self, state):
        '''
        :param state: A reference to a State (from state.py) instance which
                      holds all the information about the tasks, workers, etc. 
        '''
        self.strategy = NaiveStrategy(state)
    
    def autoscale(self):
        self.spawn(self.strategy.workers_to_spawn())
        self.kill(self.strategy.workers_to_spawn())

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