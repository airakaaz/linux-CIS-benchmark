from . import filesystem
from . import package_management
from . import apparmor
from . import bootloader
from . import process_hardening
from . import warning_banners
from . import gdm

rules = []
rules.extend(filesystem.rules)
rules.extend(package_management.rules)
rules.extend(apparmor.rules)
rules.extend(bootloader.rules)
rules.extend(process_hardening.rules)
rules.extend(warning_banners.rules)
rules.extend(gdm.rules)
