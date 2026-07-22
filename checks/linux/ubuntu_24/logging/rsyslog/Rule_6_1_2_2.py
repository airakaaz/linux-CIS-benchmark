from ._Base_6_1_2 import EnabledServiceRule


class Rule_6_1_2_2(EnabledServiceRule):
    rule_id = "6.1.2.2"
    title = "Ensure rsyslog service is enabled and active"
    workstation_lvl = 1
    server_lvl = 1

    _SERVICE = "rsyslog.service"
    _CHECK_ACTIVE = True
