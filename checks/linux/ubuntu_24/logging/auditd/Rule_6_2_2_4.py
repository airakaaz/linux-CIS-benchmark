from core import ScanResult
from ._Base_6_2_2 import AuditdOptionRule
from utils import audit


class Rule_6_2_2_4(AuditdOptionRule):
    rule_id = "6.2.2.4"
    title = "Ensure system warns when audit logs are low on space"
    workstation_lvl = 2
    server_lvl = 2
    _OPTION = "space_left_action"
    _ALLOWED = {"email", "exec", "single", "halt"}

    def check(self) -> ScanResult:
        space_left = audit.auditd_option("space_left_action")
        admin_space_left = audit.auditd_option("admin_space_left_action")
        passed = space_left in self._ALLOWED and admin_space_left in {"single", "halt"}
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "auditd low-space actions are configured correctly"
                if passed
                else "auditd low-space actions are missing or not configured correctly"
            ),
            expected="space_left_action is email, exec, single, or halt; admin_space_left_action is single or halt",
            found=f"space_left_action={space_left or 'not set'}, admin_space_left_action={admin_space_left or 'not set'}",
        )
