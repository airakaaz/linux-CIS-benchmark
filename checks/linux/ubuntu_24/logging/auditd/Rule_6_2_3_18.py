from ._Base_6_2_3 import AuditRuleSetRule


class Rule_6_2_3_18(AuditRuleSetRule):
    rule_id = "6.2.3.18"
    title = "Ensure discretionary access control permission modification events are collected"
    workstation_lvl = 2
    server_lvl = 2
    _PATTERNS = tuple(
        f"(?=.*arch={arch})(?=.*(?:{syscalls}))(?=.*auid>=\\d+)(?=.*auid!=(?:unset|-1|4294967295))(?=.*(?:key=perm_mod|-k\\s+perm_mod))"
        for arch in ("b64", "b32")
        for syscalls in (
            "chmod|fchmod|fchmodat",
            "chown|fchown|fchownat|lchown",
            "setxattr|lsetxattr|fsetxattr|removexattr|lremovexattr|fremovexattr",
        )
    )
