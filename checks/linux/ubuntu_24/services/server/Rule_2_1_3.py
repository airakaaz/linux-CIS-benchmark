from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_3(PackageNotInstalledRule):
    rule_id = "2.1.3"
    title = "Ensure avahi daemon services are not in use"
    server_lvl = 1
    workstation_lvl = 2
    _PACKAGES = ("avahi-daemon",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("avahi-daemon.service", "avahi-daemon.socket")
