from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_15(AuditRuleSetRule):
    rule_id = "6.2.3.15"
    title = "Ensure events that modify /etc/nsswitch.conf file are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = (watch("/etc/nsswitch.conf", "identity"),)
