from ._Base_6_2_4 import AuditdAccessRule, audit_log_directory, audit_log_files


class Rule_6_2_4_3(AuditdAccessRule):
    rule_id = "6.2.4.3"
    title = "Ensure audit log files owner is configured"
    workstation_lvl = 2
    server_lvl = 2

    def check(self):
        directory = audit_log_directory()
        return self.build_result(
            paths=audit_log_files(),
            valid_owners={0},
            expected="audit log files owned by root",
            missing_is_failure=directory is None or not directory.is_dir(),
            precondition_failure=(
                None
                if directory is not None and directory.is_dir()
                else "audit log directory is not set or does not exist"
            ),
        )
