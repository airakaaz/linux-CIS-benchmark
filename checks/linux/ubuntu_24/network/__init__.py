from .kernel_modules import *
from .kernel_parameters import *

rules = []
rules.extend(kernel_modules.rules)
rules.extend(kernel_parameters.rules)
