from ._Base_6_2_4 import AuditdAccessRule, audit_config_files


class Rule_6_2_4_5(AuditdAccessRule):
    rule_id = "6.2.4.5"
    title = "Ensure audit configuration files mode is configured"
    workstation_lvl = 2
    server_lvl = 2

    def check(self):
        return self.build_result(
            paths=audit_config_files(),
            max_mode=0o640,
            expected="audit configuration files mode 0640 or more restrictive",
            missing_is_failure=False,
        )
