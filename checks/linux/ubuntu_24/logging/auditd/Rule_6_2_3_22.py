from ._Base_6_2_3 import AuditRuleSetRule


class Rule_6_2_3_22(AuditRuleSetRule):
    rule_id = "6.2.3.22"
    title = "Ensure file deletion events by users are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = tuple(
        f"(?=.*arch={arch})(?=.*(?:unlink|rename|unlinkat|renameat|renameat2))(?=.*auid>=\\d+)(?=.*auid!=(?:unset|-1|4294967295))(?=.*(?:key=delete|-k\\s+delete))"
        for arch in ("b64", "b32")
    )
