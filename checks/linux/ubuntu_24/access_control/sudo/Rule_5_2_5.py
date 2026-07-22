from core import CISRule, Mode, ScanResult
from utils import sudo


class Rule_5_2_5(CISRule):
    rule_id = "5.2.5"
    title = "Ensure re-authentication for privilege escalation is not disabled globally"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        matches = sudo.active_lines(r"^.*!authenticate\b")
        passed = not matches
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="sudo re-authentication is not globally disabled" if passed else "active !authenticate sudo rules found",
            expected="no active sudoers rule contains !authenticate",
            found="none" if passed else "; ".join(matches),
        )
