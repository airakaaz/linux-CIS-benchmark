from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_16(PackageNotInstalledRule):
    rule_id = "2.1.16"
    title = "Ensure rsync services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("rsync",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("rsync.service",)
