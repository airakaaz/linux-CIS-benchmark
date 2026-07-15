from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_13(AuditRuleSetRule):
    rule_id = "6.2.3.13"
    title = "Ensure events that modify /etc/shadow and /etc/gshadow are collected"
    _PATTERNS = (watch("/etc/shadow", "identity"), watch("/etc/gshadow", "identity"))
