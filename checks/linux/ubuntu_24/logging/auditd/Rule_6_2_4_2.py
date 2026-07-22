from ._Base_6_2_4 import AuditdAccessRule, audit_log_directory, audit_log_files


class Rule_6_2_4_2(AuditdAccessRule):
    rule_id = "6.2.4.2"
    title = "Ensure audit log files mode is configured"
    workstation_lvl = 2
    server_lvl = 2

    def check(self):
        directory = audit_log_directory()
        return self.build_result(
            paths=audit_log_files(),
            max_mode=0o640,
            expected="audit log files mode 0640 or more restrictive",
            missing_is_failure=directory is None or not directory.is_dir(),
            precondition_failure=(
                None
                if directory is not None and directory.is_dir()
                else "audit log directory is not set or does not exist"
            ),
        )
