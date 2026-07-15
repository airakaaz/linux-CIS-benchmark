from collections.abc import Callable

from core import CISRule, Mode, ScanResult


class PamPolicyRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC
    _CHECK: Callable[[], tuple[bool, str]]
    _EXPECTED = ""

    def check(self) -> ScanResult:
        passed, found = self._CHECK()
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="PAM policy is configured correctly" if passed else found,
            expected=self._EXPECTED,
            found=found,
        )
