from ._Base_6_2_3 import AuditRuleSetRule


class Rule_6_2_3_2(AuditRuleSetRule):
    rule_id = "6.2.3.2"
    title = "Ensure actions as another user are always logged"
    _PATTERNS = (
        r"(?=.*arch=b64)(?=.*execve)(?=.*(?:euid!=uid|uid!=euid))(?=.*auid!=(?:unset|-1|4294967295))(?=.*(?:key=user_emulation|-k\s+user_emulation))",
        r"(?=.*arch=b32)(?=.*execve)(?=.*(?:euid!=uid|uid!=euid))(?=.*auid!=(?:unset|-1|4294967295))(?=.*(?:key=user_emulation|-k\s+user_emulation))",
    )
