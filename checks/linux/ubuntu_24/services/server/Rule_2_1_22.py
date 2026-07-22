from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_22(PackageNotInstalledRule):
    rule_id = "2.1.22"
    title = "Ensure xinetd services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("xinetd",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("xinetd.service",)
