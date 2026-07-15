from collections.abc import Callable

from core import CISRule, Mode, ScanResult


class AccountDatabaseRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC
    _CHECK: Callable[[], list[str]]
    _EXPECTED = "no account database violations"

    def check(self) -> ScanResult:
        issues = self._CHECK()
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=not issues,
            message=(
                "account database is correctly configured"
                if not issues
                else "; ".join(issues)
            ),
            expected=self._EXPECTED,
            found="none" if not issues else "; ".join(issues),
        )
