from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_19(PackageNotInstalledRule):
    rule_id = "2.1.19"
    title = "Ensure telnet server services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("^telnetd", "^telnetd-ssl")
    _MODE = "l"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("inetutils-inetd.service",)
