from ._Base_6_2_1 import VerifyInstalledRule


class Rule_6_2_1_1(VerifyInstalledRule):
    rule_id = "6.2.1.1"
    title = "Ensure auditd packages are installed"
    workstation_lvl = 2
    server_lvl = 2

    _PACKAGES = {"auditd", "audispd-plugins"}
