from core import CISRule, Mode, ScanResult
from utils import audit


class AuditdOptionRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC
    _OPTION = ""
    _ALLOWED: set[str] = set()

    def is_compliant(self, value: str | None) -> bool:
        return value in self._ALLOWED

    def expected_value(self) -> str:
        return f"{self._OPTION} = {sorted(self._ALLOWED)}"

    def check(self) -> ScanResult:
        value = audit.auditd_option(self._OPTION)
        passed = self.is_compliant(value)
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                f"{self._OPTION} is configured correctly"
                if passed
                else f"{self._OPTION} is missing or not configured correctly"
            ),
            expected=self.expected_value(),
            found=value or "not set",
        )
