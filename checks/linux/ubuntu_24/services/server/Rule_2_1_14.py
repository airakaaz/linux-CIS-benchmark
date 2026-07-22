from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_14(PackageNotInstalledRule):
    rule_id = "2.1.14"
    title = "Ensure print server services are not in use"
    workstation_lvl = 2
    server_lvl = 1
    _PACKAGES = ("cups",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("cups.socket", "cups.service")
