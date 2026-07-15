from . import devices
from . import kernel_modules
from . import kernel_parameters

rules = []
rules.extend(devices.rules)
rules.extend(kernel_modules.rules)
rules.extend(kernel_parameters.rules)
