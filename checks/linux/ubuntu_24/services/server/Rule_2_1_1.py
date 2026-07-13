from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_1(PackageNotInstalledRule):
    rule_id = "2.1.1"
    title = "Ensure autofs services are not in use"
    _PACKAGES = ("autofs",)
    _MODE = "s"
    _SERVICES = ("autofs.service",)
