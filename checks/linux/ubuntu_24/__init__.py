from . import initial_setup
from . import maintenance
from . import services
from . import network
from . import access_control
from . import firewall

rules = []
rules.extend(initial_setup.rules)
rules.extend(maintenance.rules)
rules.extend(services.rules)
rules.extend(network.rules)
rules.extend(access_control.rules)
rules.extend(firewall.rules)
