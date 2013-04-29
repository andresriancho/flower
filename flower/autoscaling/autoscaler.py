import logging

from pprint import pformat

from settings import StrategyKlass, EnforcerKlass


class Autoscaler(object):
    '''
    This class is used to make two very different concepts independent:
        * Strategies: Which define when to spawn or kill an instance
        * Enforcers: Which define HOW to spawn or kill an instance
    '''
    
    # For now we only support ampq
    SUPPORTED_TRANSPORTS = ('amqp',)
    
    def __init__(self, state):
        '''
        :param state: A reference to a State (from state.py) instance which
                      holds all the information about the tasks, workers, etc. 
        '''
        try:
            transport = state._celery_app.connection().transport.driver_type
        except AttributeError:
            # Celery versions prior to 3 don't have driver_type
            transport = None
        
        transport_supported = transport in self.SUPPORTED_TRANSPORTS

        self._can_autoscale = state._broker_api and transport_supported
         
        if not self._can_autoscale:
            supported_str = ' '.join(self.SUPPORTED_TRANSPORTS)
            logging.warning("Broker info (--broker_api) is required to be "
                            "able to auto-scale Celery worker instances."
                            " Also please note that the supported transports "
                            " for autoscaling are %s." % supported_str)
        
        self.strategy = StrategyKlass(state)
        self.enforcer = EnforcerKlass()
    
    def autoscale(self):
        if not self._can_autoscale:
            return
        
        logging.debug('Starting autoscaling')
        
        to_spawn_num = self.strategy.workers_to_spawn()
        msg = '%s determined that %s workers need to be spawned.'
        logging.debug(msg % (self.strategy.name, to_spawn_num))

        if to_spawn_num:
            self.enforcer.spawn(to_spawn_num)
        else:
            # Only try to kill if there was nothing to spawn
            
            to_kill_names = self.strategy.workers_to_kill()
            msg = '%s determined that these workers need to be killed: %s'
            logging.debug(msg % (self.strategy.name, pformat(to_kill_names)))
            
            if to_kill_names:
                self.enforcer.kill(to_kill_names)

