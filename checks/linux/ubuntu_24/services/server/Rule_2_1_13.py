from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_13(PackageNotInstalledRule):
    rule_id = "2.1.13"
    title = "Ensure nis server services are not in use"
    _PACKAGES = ("ypserv",)
    _MODE = "s"
    _SERVICES = ("ypserv.service",)
