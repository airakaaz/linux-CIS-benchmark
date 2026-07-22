from core import CISRule, Mode, ScanResult
from utils import package


class Rule_5_2_1(CISRule):
    rule_id = "5.2.1"
    title = "Ensure sudo is installed"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    _PACKAGES = ("sudo", "sudo-ldap")

    def check(self) -> ScanResult:
        passed = any(package.installed(pkg).valid for pkg in self._PACKAGES)

        if passed:
            message = "sudo is installed"
        else:
            message = "sudo is not installed"

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
        )
