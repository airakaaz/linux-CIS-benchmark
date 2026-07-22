from core import CISRule, Mode, ScanResult
from utils import filesystem


class Rule_7_1_12(CISRule):
    rule_id = "7.1.12"
    title = "Ensure no files or directories without an owner and a group exist"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        unowned, ungrouped = filesystem.unowned_paths()
        passed = not unowned and not ungrouped
        issues = [
            *(f"unowned: {path}" for path in unowned),
            *(f"ungrouped: {path}" for path in ungrouped),
        ]
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="all files and directories have an owner and group" if passed else "; ".join(issues),
            expected="no files or directories without a valid owner or group",
            found="none" if passed else "; ".join(issues),
        )
