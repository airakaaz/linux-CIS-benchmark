from core import CISRule, Mode, ScanResult
from utils import sysctl


class KernelParamRule(CISRule):
    rule_id = ""
    _PARAM = ""
    _ALLOW: set[str] = set()
    # Only set this True on rules whose audit text explicitly documents the
    # "if the UFW set value is displayed and correct, this is a passing
    # state" note (e.g. 1.5.3). Leave False (default) for rules whose audit
    # doesn't mention it (e.g. 1.5.1), even though both scripts read the
    # UFW file.
    _UFW_OVERRIDE_NOTE: bool = False
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        loaded = sysctl.get(self._PARAM)

        persistent_setting = sysctl.get_persistent(self._PARAM)
        persistent_source = persistent_setting.source
        persistent = persistent_setting.value

        ufw_file = sysctl.get_ufw_sysctl_file()
        ufw_value = (
            sysctl.get_value_from_file(self._PARAM, ufw_file)
            if ufw_file is not None
            else None
        )

        if self._UFW_OVERRIDE_NOTE and ufw_value is not None:
            persistent = ufw_value
            persistent_source = ufw_file
            passed = (
                loaded is not None
                and loaded in self._ALLOW
                and ufw_value in self._ALLOW
            )
        else:
            passed = (loaded in self._ALLOW or loaded is None) and (
                persistent in self._ALLOW or persistent is None
            )

        expected = (
            f"runtime: {self._PARAM} = {self._ALLOW}; "
            f"persistent: {self._PARAM} = {self._ALLOW}"
        )
        found = (
            f"runtime: {self._PARAM} = {loaded}; "
            f"persistent: {self._PARAM} = {persistent}"
            + (f" (source: {persistent_source})" if persistent_source else "")
        )
        message = (
            f"{self._PARAM} is correctly loaded and persistent."
            if passed
            else f"{self._PARAM} is not correctly loaded and/or configured."
        )
        if (
            self._UFW_OVERRIDE_NOTE
            and ufw_value is not None
            and ufw_value not in self._ALLOW
        ):
            message += f" UFW sets an incorrect value in {ufw_file}; update it there."

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
            expected=expected,
            found=found,
        )
