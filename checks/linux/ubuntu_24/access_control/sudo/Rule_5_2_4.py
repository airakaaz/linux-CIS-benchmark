from core import CISRule, Mode, ScanResult
from utils import sudo


class Rule_5_2_4(CISRule):
    rule_id = "5.2.4"
    title = "Ensure users must provide password for escalation"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        matches = sudo.active_lines(r"^.*\bNOPASSWD\b")
        passed = not matches
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="sudo requires a password for escalation" if passed else "active NOPASSWD sudo rules found",
            expected="no active sudoers rule contains NOPASSWD",
            found="none" if passed else "; ".join(matches),
        )
