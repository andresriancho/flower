import textwrap
import logging

from pprint import pformat

from settings import MIN_WORKERS, MAX_WORKERS
from ..models import WorkersModel


class BaseStrategy(object):
    '''
    Base strategy, provides utility methods such as `get_idle_workers` and
    defines which methods need to be implemented in subclasses:
        * workers_to_spawn
        * workers_to_kill
    '''
    name = 'Base strategy'
    
    def __init__(self, state):
        '''
        :param state: A reference to a State (from state.py) instance which
                      holds all the information about the tasks, workers, etc. 
        '''
        self.state = state
    
    def workers_to_spawn(self):
        '''
        :return: An integer with the number of workers to be spawned.
        '''
        raise NotImplemented
    
    def workers_to_kill(self):
        '''
        :return: A list with the names of the workers that need to be killed
        '''
        raise NotImplemented

    def get_idle_workers(self):
        '''
        :return: A list with the names of the idle workers
        '''
        idle_workers = []
        
        app = self.state.celery_app
        workers = WorkersModel.get_latest(app).workers
        
        for name, info in workers.iteritems():
            if info['running_tasks'] == 0:
                idle_workers.append(name)
        
        logging.debug('Idle workers: %s' % pformat(idle_workers))
        
        return idle_workers
    
    def get_description(self):
        return textwrap.dedent(self.__doc__).strip()


class NaiveStrategy(object):
    '''
    Very naive strategy which will create a new worker when there are queued
    tasks in the broker, and kill workers when they are not running any task.
    '''
    
    name = 'Naive strategy'
    
    def workers_to_spawn(self):
        workers_to_spawn = 0
        registered_tasks_len = len(self.state.registered_tasks)
        
        if registered_tasks_len >= 1:
            workers_to_spawn = registered_tasks_len
        
        msg = 'Naive strategy determined that %s workers need to be spawned.'
        logging.debug(msg % workers_to_spawn)
        
        return workers_to_spawn
    
    def workers_to_kill(self):
        
        workers_to_kill = self.get_idle_workers()
        
        msg = 'Naive strategy determined that %s need to be killed.'
        logging.debug(msg % pformat(workers_to_kill))

        return workers_to_kill