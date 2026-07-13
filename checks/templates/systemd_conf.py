from core import CISRule, Mode, ScanResult
from utils import systemd


class SystemdConfOptionRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _CONF_UNIT = ""
    _SECTION = ""
    _OPTION = ""
    _ALLOW: set[str] = set()

    def check(self) -> ScanResult:
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
