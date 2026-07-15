from core import CISRule, Mode, ScanResult
from utils import logfiles


class LogfileAccessRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        issues = logfiles.permission_issues()
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=not issues,
            message="all log files have appropriate permissions and ownership" if not issues else "; ".join(issues),
            expected="/var/log files comply with their CIS mode, owner, and group policy",
            found="none" if not issues else "; ".join(issues),
        )
