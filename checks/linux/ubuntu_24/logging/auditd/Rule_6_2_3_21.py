from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_21(AuditRuleSetRule):
    rule_id = "6.2.3.21"
    title = "Ensure login and logout events are collected"
    _PATTERNS = (
        watch("/var/log/lastlog", "logins"),
        watch("/var/run/faillock", "logins"),
    )
