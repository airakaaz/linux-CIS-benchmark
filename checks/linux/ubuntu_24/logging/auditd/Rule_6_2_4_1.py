from ._Base_6_2_4 import AuditdAccessRule, audit_log_directory


class Rule_6_2_4_1(AuditdAccessRule):
    rule_id = "6.2.4.1"
    title = "Ensure the audit log file directory mode is configured"

    def check(self):
        directory = audit_log_directory()
        return self.build_result(
            paths=[directory] if directory is not None else [],
            max_mode=0o750,
            expected="audit log directory mode 0750 or more restrictive",
            precondition_failure=(
                None
                if directory is not None and directory.is_dir()
                else "audit log directory is not set or does not exist"
            ),
        )
