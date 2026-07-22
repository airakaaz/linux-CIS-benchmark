from core import CISRule, Mode, ScanResult
from utils import sudo


class Rule_5_2_3(CISRule):
    rule_id = "5.2.3"
    title = "Ensure sudo log file exists"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        path = sudo.logfile()
        passed = bool(path)
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="sudo has a custom logfile configured" if passed else "sudo logfile is not configured",
            expected="Defaults logfile points to a custom log file",
            found=path or "not configured",
        )
