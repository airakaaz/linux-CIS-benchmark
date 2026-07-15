from ._Base_3_1 import PackageNotInstalledRule


class Rule_3_1_3(PackageNotInstalledRule):
    rule_id = "3.1.3"
    title = "Ensure bluetooth services are not in use"
    _PACKAGES = ("bluez",)
    _ALLOW_AS_DEPENDENCY = True
    _MODE = "s"
    _SERVICES = ("bluetooth.service",)
