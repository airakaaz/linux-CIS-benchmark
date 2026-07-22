from ._Base_6_1_2 import VerifyInstalledRule


class Rule_6_1_2_1(VerifyInstalledRule):
    rule_id = "6.1.2.1"
    title = "Ensure rsyslog is installed"
    workstation_lvl = 1
    server_lvl = 1

    _PACKAGES = {"rsyslog"}
