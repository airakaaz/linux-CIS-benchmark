from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_21(PackageNotInstalledRule):
    rule_id = "2.1.21"
    title = "Ensure web proxy server services are not in use"
    _PACKAGES = ("squid",)
    _MODE = "s"
    _SERVICES = ("squid.service",)
