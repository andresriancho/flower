from .base import BaseStrategy


class NaiveStrategy(BaseStrategy):
    '''
    Very naive strategy which will create a new worker when there are queued
    tasks in the broker, and kill workers when they are not running any task.
    '''
    
    MIN_WORKERS = 1
    MAX_WORKERS = 100
    MAX_SPAWNS = 10
    
    name = 'Naive strategy'
    
    def workers_to_spawn(self):
        if len(self.get_all_workers()) < self.MIN_WORKERS:
            return self.MIN_WORKERS
        
        if len(self.get_all_workers()) == self.MAX_WORKERS:
            return 0
            
        queued_tasks = self.get_queued_tasks()
        
        workers_to_spawn = min(queued_tasks, self.MAX_SPAWNS)
        
        return workers_to_spawn
    
    def workers_to_kill(self):
        
        workers_to_kill = self.get_idle_workers()
        
        return workers_to_kill