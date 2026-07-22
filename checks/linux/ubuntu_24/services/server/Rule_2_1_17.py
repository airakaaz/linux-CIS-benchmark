from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_17(PackageNotInstalledRule):
    rule_id = "2.1.17"
    title = "Ensure samba file server services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("samba",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("smbd.service",)
