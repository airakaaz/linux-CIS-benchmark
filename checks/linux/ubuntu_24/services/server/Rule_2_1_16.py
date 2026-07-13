from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_16(PackageNotInstalledRule):
    rule_id = "2.1.16"
    title = "Ensure rsync services are not in use"
    _PACKAGES = ("rsync",)
    _MODE = "s"
    _SERVICES = ("rsync.service",)
