from core import ScanResult
from ._Base_6_2_2 import AuditdOptionRule
from utils import audit


class Rule_6_2_2_3(AuditdOptionRule):
    rule_id = "6.2.2.3"
    title = "Ensure system is disabled when audit logs are full"
    workstation_lvl = 2
    server_lvl = 2
    _OPTION = "disk_full_action"
    _ALLOWED = {"halt", "single"}

    def check(self) -> ScanResult:
        full = audit.auditd_option("disk_full_action")
        error = audit.auditd_option("disk_error_action")
        passed = full in {"halt", "single"} and error in {"syslog", "single", "halt"}
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "auditd disk-full and disk-error actions are configured correctly"
                if passed
                else "auditd disk-full and/or disk-error actions are not configured correctly"
            ),
            expected="disk_full_action is halt or single; disk_error_action is syslog, single, or halt",
            found=f"disk_full_action={full or 'not set'}, disk_error_action={error or 'not set'}",
        )
