from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_8(PackageNotInstalledRule):
    rule_id = "2.1.8"
    title = "Ensure ftp server services are not in use"
    _PACKAGES = ("vsftpd",)
    _MODE = "s"
    _SERVICES = ("vsftpd.service",)
