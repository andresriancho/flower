from .strategies.naive import NaiveStrategy
from .enforcers.ec2 import Ec2Enforcer

# TODO: This should be configurable from the web UI
StrategyKlass = NaiveStrategy
EnforcerKlass = Ec2Enforcer

