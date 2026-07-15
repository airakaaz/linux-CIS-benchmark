from ._Base_6_2_3 import AuditRuleSetRule, executable


class Rule_6_2_3_24(AuditRuleSetRule):
    rule_id = "6.2.3.24"
    title = "Ensure successful and unsuccessful attempts to use the chcon command are collected"
    _PATTERNS = (executable("/usr/bin/chcon", "perm_chng"),)
