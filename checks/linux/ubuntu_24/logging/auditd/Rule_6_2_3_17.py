from ._Base_6_2_3 import AuditRuleSetRule


class Rule_6_2_3_17(AuditRuleSetRule):
    rule_id = "6.2.3.17"
    title = "Ensure unsuccessful file access attempts are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = tuple(
        f"(?=.*arch={arch})(?=.*(?:creat|open|openat|truncate|ftruncate))(?=.*exit={result})(?=.*auid>=\\d+)(?=.*auid!=(?:unset|-1|4294967295))(?=.*(?:key=access|-k\\s+access))"
        for arch in ("b64", "b32")
        for result in ("-EACCES", "-EPERM")
    )
