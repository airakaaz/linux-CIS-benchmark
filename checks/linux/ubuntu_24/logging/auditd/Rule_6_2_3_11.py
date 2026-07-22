from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_11(AuditRuleSetRule):
    rule_id = "6.2.3.11"
    title = "Ensure events that modify /etc/group information are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = (watch("/etc/group", "identity"),)
