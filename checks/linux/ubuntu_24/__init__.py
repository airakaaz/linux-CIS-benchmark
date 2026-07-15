from . import initial_setup
from . import services
from . import network
from . import firewall
from . import access_control
from . import logging
from . import maintenance

rules = []
rules.extend(initial_setup.rules)
rules.extend(services.rules)
rules.extend(network.rules)
rules.extend(firewall.rules)
rules.extend(access_control.rules)
rules.extend(logging.rules)
rules.extend(maintenance.rules)
