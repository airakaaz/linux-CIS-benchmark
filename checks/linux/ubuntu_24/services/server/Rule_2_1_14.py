from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_14(PackageNotInstalledRule):
    rule_id = "2.1.14"
    title = "Ensure print server services are not in use"
    _PACKAGES = ("cups",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("cups.socket", "cups.service")
