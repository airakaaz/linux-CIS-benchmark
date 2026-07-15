from checks.templates.verify_installed import VerifyInstalledRule
from checks.templates.service_status import EnabledServiceRule

from core import CISRule, Mode, ScanResult
from utils import grub


class GrubAuditParameterRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC
    _PARAMETER = ""
    _PATTERN = None

    def check(self) -> ScanResult:
        lines = grub.linux_cmdlines()
        missing = [line for line in lines if not self._PATTERN.search(line)]
        passed = bool(lines) and not missing
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                f"all Linux boot entries configure {self._PARAMETER}"
                if passed
                else f"{self._PARAMETER} is missing from one or more Linux boot entries"
            ),
            expected=f"every Linux boot entry contains {self._PARAMETER}",
            found=f"{len(lines) - len(missing)}/{len(lines)} entries compliant",
        )
