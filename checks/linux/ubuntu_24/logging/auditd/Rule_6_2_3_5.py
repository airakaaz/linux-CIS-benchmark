from ._Base_6_2_3 import AuditRuleSetRule


class Rule_6_2_3_5(AuditRuleSetRule):
    rule_id = "6.2.3.5"
    title = "Ensure events that modify sethostname and setdomainname are collected"
    _PATTERNS = (
        r"(?=.*arch=b64)(?=.*sethostname)(?=.*setdomainname)(?=.*(?:key=system-locale|-k\s+system-locale))",
        r"(?=.*arch=b32)(?=.*sethostname)(?=.*setdomainname)(?=.*(?:key=system-locale|-k\s+system-locale))",
    )
