from ._Base_6_2_4 import AuditdAccessRule, audit_config_files


class Rule_6_2_4_6(AuditdAccessRule):
    rule_id = "6.2.4.6"
    title = "Ensure audit configuration files owner is configured"
    workstation_lvl = 2
    server_lvl = 2

    def check(self):
        return self.build_result(
            paths=audit_config_files(),
            valid_owners={0},
            expected="audit configuration files owned by root",
            missing_is_failure=False,
        )
