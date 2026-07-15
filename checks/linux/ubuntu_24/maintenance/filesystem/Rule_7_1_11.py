from core import CISRule, Mode, ScanResult
from utils import filesystem


class Rule_7_1_11(CISRule):
    rule_id = "7.1.11"
    title = "Ensure world writable files and directories are secured"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        files, directories = filesystem.world_writable_paths()
        passed = not files and not directories
        issues = [
            *(f"world writable file: {path}" for path in files),
            *(f"world writable directory without sticky bit: {path}" for path in directories),
        ]
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="world writable files and directories are secured" if passed else "; ".join(issues),
            expected="no world writable files and no world writable directories without the sticky bit",
            found="none" if passed else "; ".join(issues),
        )
