from core import CISRule, Mode, ScanResult
from utils import package, systemctl


class EnabledServiceRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _SERVICE: str = "ufw.service"
    _CHECK_ACTIVE: bool = False
    _PACKAGE: str | None = None
    _PASS_ON_MISSING: bool = True

    def check(self) -> ScanResult:
        if self._PACKAGE is not None:
            if package.not_installed(self._PACKAGE):
                return ScanResult(
                    rule_id=self.rule_id,
                    title=self.title,
                    passed=self._PASS_ON_MISSING,
                    message=f"{self._PACKAGE} not available on the system",
                    expected="N/A",
                    found=f"{self._PACKAGE} not installed",
                )

        enabled = systemctl.is_enabled(self._SERVICE)

        expected = f"{self._SERVICE} is enabled"
        found = f"{self._SERVICE} is" + (" enabled" if enabled else " not enabled")

        if self._CHECK_ACTIVE:
            active = systemctl.is_active(self._SERVICE) if self._CHECK_ACTIVE else True
            expected = f"{self._SERVICE} is enabled and active"
            found += " and is " + ("active" if active else "not active")
            passed = enabled and active
        else:
            passed = enabled

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                f"service {self._SERVICE} is enabled properly"
                if passed
                else f"service {self._SERVICE} is not enabled properly"
            ),
            expected=expected,
            found=found,
        )
