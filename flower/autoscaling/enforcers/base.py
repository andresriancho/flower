class BaseEnforcer(object):
    
    def spawn(self, number):
        '''
        :param number: The number of workers which will be spawned
        '''    
        raise NotImplementedError
    
    def kill(self, workers):
        '''
        :param workers: The names of the workers to be killed
        '''    
        raise NotImplementedError