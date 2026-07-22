from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_15(PackageNotInstalledRule):
    rule_id = "2.1.15"
    title = "Ensure rpcbind services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("rpcbind",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("rpcbind.socket", "rpcbind.service")
