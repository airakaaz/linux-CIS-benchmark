from core import CISRule, Mode, ScanResult
from utils import package


class Rule_1_3_1_1(CISRule):
    rule_id = "1.3.1.1"
    title = "Ensure apparmor packages are installed"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        missing = package.missing("apparmor", "apparmor-utils")

        if missing:
            message = f"package(s) ({', '.join(missing)}) missing"
        else:
            message = "apparmor and apparmor-utils are installed"

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=missing == [],
            message=message,
        )
