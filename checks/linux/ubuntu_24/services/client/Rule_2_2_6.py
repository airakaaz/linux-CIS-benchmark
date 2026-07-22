from ._Base_2_2 import VerifyNotInstalledRule


class Rule_2_2_6(VerifyNotInstalledRule):
    rule_id = "2.2.6"
    _PACKAGES = {"ftp", "tnftp"}
    title = "Ensure ftp client is not installed"
    workstation_lvl = 1
    server_lvl = 1
