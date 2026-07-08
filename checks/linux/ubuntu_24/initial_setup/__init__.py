from .filesystem import *
from .package_management import *

rules = []
rules.extend(filesystem.rules)
rules.extend(package_management.rules)
