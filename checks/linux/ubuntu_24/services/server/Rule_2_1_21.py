from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_21(PackageNotInstalledRule):
    rule_id = "2.1.21"
    title = "Ensure web proxy server services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("squid",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("squid.service",)
