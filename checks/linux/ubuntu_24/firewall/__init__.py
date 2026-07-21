from core.module import Module

from .ufw import ufw

subMods = [
    ufw,
]

firewall = Module(name="firewall", subMods=subMods)
