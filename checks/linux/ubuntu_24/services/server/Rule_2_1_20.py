from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_20(PackageNotInstalledRule):
    rule_id = "2.1.20"
    title = "Ensure tftp server services are not in use"
    workstation_lvl = 1
    server_lvl = 1
    _PACKAGES = ("tftpd-hpa",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("tftpd-hpa.service",)
