from core.module import Module

from .initial_setup import initial_setup
from .services import services
from .network import network
from .firewall import firewall
from .access_control import access_control
from .logging import logging
from .maintenance import maintenance

subMods = []
subMods.append(initial_setup)
subMods.append(services)
subMods.append(network)
subMods.append(firewall)
subMods.append(access_control)
subMods.append(logging)
subMods.append(maintenance)


ubuntu_24 = Module(name="ubuntu_24", subMods=subMods)
