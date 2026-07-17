from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_7(PackageNotInstalledRule):
    rule_id = "2.1.7"
    title = "Ensure dns server services are not in use"
    _PACKAGES = ("bind9",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("named.service",)
