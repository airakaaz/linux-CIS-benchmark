from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_1(AuditRuleSetRule):
    rule_id = "6.2.3.1"
    title = "Ensure changes to system administration scope (sudoers) is collected"
    _PATTERNS = (watch("/etc/sudoers", "scope"), watch("/etc/sudoers.d", "scope"))
