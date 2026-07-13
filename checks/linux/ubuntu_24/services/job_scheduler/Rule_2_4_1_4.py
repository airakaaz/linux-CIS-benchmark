from core import ScanResult
from utils import package
from ._Base_2_4_1 import PathAccessRule


class Rule_2_4_1_4(PathAccessRule):
    rule_id = "2.4.1.4"

    _PATH = "/etc/cron.daily/"
    _MAX_ACCESS = 0o700

    title = f"Ensure access to {_PATH} is configured"

    def check(self) -> ScanResult:
        if package.installed("cron").valid:
            return super().check()
        else:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message="cron not installed in this system",
                expected="N/A",
                found="cron not installed",
            )
