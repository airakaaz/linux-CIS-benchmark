from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_5(PackageNotInstalledRule):
    rule_id = "2.1.5"
    title = "Ensure dhcp services services are not in use"
    _PACKAGES = ("kea",)
    _MODE = "l"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = (
        "kea-dhcp-ddns-server.service",
        "kea-dhcp4-server.service",
        "kea-dhcp6-server.service",
    )
