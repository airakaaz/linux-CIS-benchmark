from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_16(AuditRuleSetRule):
    rule_id = "6.2.3.16"
    title = "Ensure events that modify /etc/pam.conf and /etc/pam.d/ information are collected"
    _PATTERNS = (watch("/etc/pam.conf", "identity"), watch("/etc/pam.d", "identity"))
