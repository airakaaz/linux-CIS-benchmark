from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_8(AuditRuleSetRule):
    rule_id = "6.2.3.8"
    title = "Ensure events that modify /etc/network and /etc/networks are collected"
    _PATTERNS = (watch("/etc/network", "system-locale"), watch("/etc/networks", "system-locale"))
