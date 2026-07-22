from core import CISRule, Mode, ScanResult
from ._Base_6_2_3 import sudo_log_file, watch
from utils import audit


class Rule_6_2_3_3(CISRule):
    rule_id = "6.2.3.3"
    title = "Ensure events that modify the sudo log file are collected"
    workstation_lvl = 2
    server_lvl = 2
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        path = sudo_log_file()
        state = audit.audit_rule_state(watch(path, "sudo_log_file")) if path else None
        passed = state is not None and state.valid
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "sudo logfile is configured and audited"
                if passed
                else "sudo logfile is not configured or is not audited"
            ),
            expected="sudo logfile exists and is watched with key sudo_log_file in both configurations",
            found=(
                f"{path}: running={state.running}, persistent={state.persistent}"
                if state is not None
                else "sudo logfile not configured"
            ),
        )
