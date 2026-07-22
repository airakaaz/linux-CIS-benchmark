from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_20(AuditRuleSetRule):
    rule_id = "6.2.3.20"
    title = "Ensure session initiation information is collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = (
        watch("/var/run/utmp", "session"),
        watch("/var/log/wtmp", "session"),
        watch("/var/log/btmp", "session"),
    )
