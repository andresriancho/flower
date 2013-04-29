import textwrap
import logging

from pprint import pformat


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
        raise NotImplementedError
    
    def workers_to_kill(self):
        '''
        :return: A list with the names of the workers that need to be killed
        '''
        raise NotImplementedError

    def get_idle_workers(self):
        '''
        :return: A list with the names of the idle workers
        '''
        idle_workers = []
        
        for name, info in self.state.active_tasks.iteritems():
            if len(info) == 0:
                idle_workers.append(name)
        
        logging.debug('Idle workers: %s' % pformat(idle_workers))
        
        return idle_workers
    
    def get_all_workers(self):
        return self.state.active_tasks.keys()
    
    def get_busy_workers(self):
        '''
        :return: A list with the names of the busy workers
        '''
        busy_workers = []
        
        for name, info in self.state.active_tasks.iteritems():
            if len(info) != 0:
                busy_workers.append(name)
        
        logging.debug('Busy workers: %s' % pformat(busy_workers))
        
        return busy_workers
    
        
    def get_queued_tasks(self):
        '''
        :return: An integer with the number of queued tasks in the broker
        '''
        queued_tasks = 0
        
        for queue_information in self.state.broker_queues:
            queued_tasks += queue_information.get('messages')

        logging.debug('Queued tasks: %s' % queued_tasks)

        return queued_tasks
    
    def get_description(self):
        return textwrap.dedent(self.__doc__).strip()


