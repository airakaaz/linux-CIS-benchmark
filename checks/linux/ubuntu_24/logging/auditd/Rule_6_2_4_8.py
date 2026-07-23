from ._Base_6_2_4 import AUDIT_TOOLS, AuditdAccessRule


class Rule_6_2_4_8(AuditdAccessRule):
    rule_id = "6.2.4.8"
    title = "Ensure audit tools mode is configured"
    workstation_lvl = 2
    server_lvl = 2

    def check(self):
        return self.build_result(
            paths=list(AUDIT_TOOLS),
            max_mode=0o755,
            expected="audit tools mode 0755 or more restrictive",
            missing_is_failure=False,
        )
