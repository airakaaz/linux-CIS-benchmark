from core import CISRule, Mode, ScanResult
from utils import package, systemctl


class Rule_2_4_1_1(CISRule):
    rule_id = "2.4.1.1"
    title = "Ensure cron daemon is enabled and active"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    _PACKAGE = "cron"
    _SERVICE_NAMES = ("cron.service", "crond.service")

    def check(self) -> ScanResult:
        if package.not_installed(self._PACKAGE).valid:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message=f"{self._PACKAGE} is not installed; not applicable.",
                expected="N/A",
                found=f"{self._PACKAGE} not installed",
            )

        enabled = any(systemctl.is_enabled(name) for name in self._SERVICE_NAMES)
        active = any(systemctl.is_active(name) for name in self._SERVICE_NAMES)

        passed = enabled and active

        issues = []
        if not enabled:
            issues.append("not enabled")
        if not active:
            issues.append("not active")

        message = (
            "cron service is enabled and active."
            if passed
            else f"cron service is {' and '.join(issues)}."
        )

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
            expected="cron.service or crond.service enabled and active",
            found=f"enabled={enabled}, active={active}",
        )
