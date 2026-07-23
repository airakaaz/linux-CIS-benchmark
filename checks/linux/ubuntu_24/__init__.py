from core import Module, CISRule
from enum import Enum


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


class level(Enum):
    server_1 = "server_1"
    server_2 = "server_2"
    workstation_1 = "workstation_1"
    workstation_2 = "workstation_2"


def mod_filter(modules: list[Module], lvl: level) -> list[Module]:
    filtered_modules = []
    for mod in modules:
        match lvl:
            case level.server_1:
                buf = [r for r in mod.rules if r.server_lvl == 1]
            case level.server_2:
                buf = [r for r in mod.rules if r.server_lvl]
            case level.workstation_1:
                buf = [r for r in mod.rules if r.workstation_lvl == 1]
            case level.workstation_2:
                buf = [r for r in mod.rules if r.workstation_lvl]
        filtered_modules.append(Module(mod.name, rules=buf))
    return filtered_modules


ubuntu_24 = Module(name="ubuntu_24", subMods=subMods)
ubuntu_24.levels = {
    "server 1": level.server_1,
    "server 2": level.server_2,
    "workstation 1": level.workstation_1,
    "workstation 2": level.workstation_2,
}
ubuntu_24.filter = mod_filter
