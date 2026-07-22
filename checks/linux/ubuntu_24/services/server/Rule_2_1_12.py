from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_12(PackageNotInstalledRule):
    rule_id = "2.1.12"
    title = "Ensure network file system services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("nfs-kernel-server",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("nfs-server.service",)
