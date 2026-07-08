from .initial_setup import *
from .maintenance import *
from .services import *

rules = []
rules.extend(initial_setup.rules)
rules.extend(maintenance.rules)
rules.extend(services.rules)
