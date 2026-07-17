from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_9(PackageNotInstalledRule):
    rule_id = "2.1.9"
    title = "Ensure dnsmasq services are not in use"
    _PACKAGES = ("dnsmasq",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("dnsmasq.service",)
