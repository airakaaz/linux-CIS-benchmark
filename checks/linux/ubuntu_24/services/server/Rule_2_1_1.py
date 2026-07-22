from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_1(PackageNotInstalledRule):
    rule_id = "2.1.1"
    title = "Ensure autofs services are not in use"
    server_lvl = 1
    workstation_lvl = 2
    _PACKAGES = ("autofs",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("autofs.service",)
