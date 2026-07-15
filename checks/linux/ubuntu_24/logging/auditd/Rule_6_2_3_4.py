from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_4(AuditRuleSetRule):
    rule_id = "6.2.3.4"
    title = "Ensure events that modify date and time information are collected"
    _PATTERNS = (
        r"(?=.*arch=b64)(?=.*(?:adjtimex|settimeofday))(?=.*(?:key=time-change|-k\s+time-change))",
        r"(?=.*arch=b32)(?=.*(?:adjtimex|settimeofday))(?=.*(?:key=time-change|-k\s+time-change))",
        r"(?=.*arch=b64)(?=.*clock_settime)(?=.*a0=0x0)(?=.*(?:key=time-change|-k\s+time-change))",
        r"(?=.*arch=b32)(?=.*clock_settime)(?=.*a0=0x0)(?=.*(?:key=time-change|-k\s+time-change))",
        watch("/etc/localtime", "time-change"),
    )
