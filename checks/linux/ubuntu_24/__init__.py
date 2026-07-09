from .initial_setup import *
from .maintenance import *
from .services import *
from .network import *

rules = []
rules.extend(initial_setup.rules)
rules.extend(maintenance.rules)
rules.extend(services.rules)
rules.extend(network.rules)
