from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_6(AuditRuleSetRule):
    rule_id = "6.2.3.6"
    title = "Ensure events that modify /etc/issue and /etc/issue.net are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = (watch("/etc/issue", "system-locale"), watch("/etc/issue.net", "system-locale"))
