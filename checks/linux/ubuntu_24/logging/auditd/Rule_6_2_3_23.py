from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_23(AuditRuleSetRule):
    rule_id = "6.2.3.23"
    title = "Ensure events that modify the system's Mandatory Access Controls are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = (watch("/etc/apparmor/", "MAC-policy"), watch("/etc/apparmor.d/", "MAC-policy"))
