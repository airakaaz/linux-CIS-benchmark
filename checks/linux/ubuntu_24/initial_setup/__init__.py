from .filesystem import *
from .package_management import *
from .apparmor import *
from .process_hardening import *
from .bootloader import *
from .warning_banners import *
from .gdm import *

rules = []
rules.extend(filesystem.rules)
rules.extend(package_management.rules)
rules.extend(apparmor.rules)
rules.extend(process_hardening.rules)
rules.extend(bootloader.rules)
rules.extend(warning_banners.rules)
rules.extend(gdm.rules)
