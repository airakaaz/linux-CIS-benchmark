from core import CISRule, Mode, ScanResult
from utils import package, systemd


class SystemdConfOptionRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _CONF_UNIT = ""
    _SECTION = ""
    _OPTION = ""
    _ALLOW: set[str] = set()
    _REQUIRED_PACKAGE: str | None = None

    def check(self) -> ScanResult:
        if self._REQUIRED_PACKAGE is not None and package.not_installed(
            self._REQUIRED_PACKAGE
        ).valid:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message=f"{self._REQUIRED_PACKAGE} is not installed; not applicable.",
                expected="N/A",
                found=f"{self._REQUIRED_PACKAGE} not installed",
            )

        setting = systemd.get_option(self._CONF_UNIT, self._SECTION, self._OPTION)
        value = setting.value
        passed = value is not None and value in self._ALLOW

        expected = f"{self._OPTION} in {sorted(self._ALLOW)}"

        if value is None:
            found = f"{self._OPTION} not set anywhere (including defaults)"
        elif setting.is_default:
            found = (
                f"{self._OPTION} = {value} (compiled-in default, from {setting.source})"
            )
        else:
            found = f"{self._OPTION} = {value} (from {setting.source})"

        message = (
            f"{self._OPTION} is correctly configured."
            if passed
            else f"{self._OPTION} is not correctly configured."
        )

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
            expected=expected,
            found=found,
        )
