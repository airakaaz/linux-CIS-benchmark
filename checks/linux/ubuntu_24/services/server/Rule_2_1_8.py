from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_8(PackageNotInstalledRule):
    rule_id = "2.1.8"
    title = "Ensure ftp server services are not in use"
    server_lvl = 1
    workstation_lvl = 1
    _PACKAGES = ("vsftpd",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("vsftpd.service",)
