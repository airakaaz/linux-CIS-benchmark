from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_12(AuditRuleSetRule):
    rule_id = "6.2.3.12"
    title = "Ensure events that modify /etc/passwd information are collected"
    _PATTERNS = (watch("/etc/passwd", "identity"),)
