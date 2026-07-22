from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_14(AuditRuleSetRule):
    rule_id = "6.2.3.14"
    title = "Ensure events that modify /etc/security/opasswd are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = (watch("/etc/security/opasswd", "identity"),)
