from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_7(AuditRuleSetRule):
    rule_id = "6.2.3.7"
    title = "Ensure events that modify /etc/hosts and /etc/hostname are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = (
        watch("/etc/hosts", "system-locale"),
        watch("/etc/hostname", "system-locale"),
    )
