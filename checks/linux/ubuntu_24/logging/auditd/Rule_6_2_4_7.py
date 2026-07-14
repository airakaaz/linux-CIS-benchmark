from ._Base_6_2_4 import AuditdAccessRule, audit_config_files


class Rule_6_2_4_7(AuditdAccessRule):
    rule_id = "6.2.4.7"
    title = "Ensure audit configuration files group owner is configured"

    def check(self):
        return self.build_result(
            paths=audit_config_files(),
            valid_groups={0},
            expected="audit configuration files group owned by root",
            missing_is_failure=False,
        )
