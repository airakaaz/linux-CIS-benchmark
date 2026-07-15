from ._Base_6_2_3 import AuditRuleSetRule, executable


class Rule_6_2_3_27(AuditRuleSetRule):
    rule_id = "6.2.3.27"
    title = "Ensure successful and unsuccessful attempts to use the usermod command are collected"
    _PATTERNS = (executable("/usr/sbin/usermod", "usermod"),)
