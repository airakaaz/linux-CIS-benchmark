from core import ScanResult

from ._Base_6_2_4 import (
    AuditdAccessRule,
    audit_log_directory,
    audit_log_files,
    audit_log_group,
    group_id,
)


class Rule_6_2_4_4(AuditdAccessRule):
    rule_id = "6.2.4.4"
    title = "Ensure audit log files group owner is configured"

    def check(self) -> ScanResult:
        configured_group = audit_log_group()
        valid_groups = {0}
        adm_gid = group_id("adm")
        if adm_gid is not None:
            valid_groups.add(adm_gid)

        directory = audit_log_directory()
        if configured_group not in {"root", "adm"}:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=False,
                message="auditd log_group is not set to root or adm",
                expected="log_group = root or adm and audit log files use that group",
                found=f"log_group = {configured_group or 'not set'}",
            )

        return self.build_result(
            paths=audit_log_files(),
            valid_groups=valid_groups,
            expected="audit log files group owned by root or adm",
            missing_is_failure=directory is None or not directory.is_dir(),
            precondition_failure=(
                None
                if directory is not None and directory.is_dir()
                else "audit log directory is not set or does not exist"
            ),
        )
