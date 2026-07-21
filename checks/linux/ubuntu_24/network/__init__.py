from core.module import Module

from .devices import devices
from .kernel_modules import kernel_modules
from .kernel_parameters import kernel_parameters

subMods = [
    devices,
    kernel_modules,
    kernel_parameters,
]

network = Module(name="network", subMods=subMods)
