from ._Base_6_2_3 import AuditRuleSetRule


class Rule_6_2_3_19(AuditRuleSetRule):
    rule_id = "6.2.3.19"
    title = "Ensure successful file system mounts are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = tuple(
        f"(?=.*arch={arch})(?=.*-S\\s+mount\\b)(?=.*auid>=\\d+)(?=.*auid!=(?:unset|-1|4294967295))(?=.*(?:key=mounts|-k\\s+mounts))"
        for arch in ("b64", "b32")
    )
