from ._Base_6_2_3 import AuditRuleSetRule, executable


class Rule_6_2_3_26(AuditRuleSetRule):
    rule_id = "6.2.3.26"
    title = "Ensure successful and unsuccessful attempts to use the chacl command are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = (executable("/usr/bin/chacl", "perm_chng"),)
