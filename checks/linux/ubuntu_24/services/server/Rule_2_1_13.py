from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_13(PackageNotInstalledRule):
    rule_id = "2.1.13"
    title = "Ensure nis server services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("ypserv",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("ypserv.service",)
