from ._Base_6_2_1 import EnabledServiceRule


class Rule_6_2_1_2(EnabledServiceRule):
    rule_id = "6.2.1.2"
    title = "Ensure auditd service is enabled and active"
    workstation_lvl = 2
    server_lvl = 2

    _SERVICE = "auditd.service"
    _CHECK_ACTIVE = True
