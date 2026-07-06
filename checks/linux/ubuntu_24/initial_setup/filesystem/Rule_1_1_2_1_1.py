from core import CISRule, ScanResult
from utils import mount, service


# rewritten cuz it needs to check if the tmp.mount is enabled
class Rule_1_1_2_1_1(CISRule):
    rule_id = "1.1.2.1.1"

    _MOUNT_POINT = "/tmp"
    _UNIT = "tmp.mount"
    _BAD_UNIT_STATES = {"masked", "disabled"}

    title = f"Ensure {_MOUNT_POINT} is tmpfs or a separate partition"

    def check(self) -> ScanResult:
        reasons = []

        options = mount.get_mount_options(self._MOUNT_POINT)
        mounted = options is not None

        if not mounted:
            reasons.append(
                f"'{self._MOUNT_POINT}' is not mounted as tmpfs or a separate partition"
            )

        enabled_state = service.get_enabled_state(self._UNIT)
        unit_ok = enabled_state not in self._BAD_UNIT_STATES

        if not unit_ok:
            reasons.append(f"'{self._UNIT}' is {enabled_state}")

        passed = mounted and unit_ok

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                f"'{self._MOUNT_POINT}' is a separate mount and '{self._UNIT}' is '{enabled_state}'."
                if passed
                else f"'{self._MOUNT_POINT}' is not properly configured: {', '.join(reasons)}."
            ),
            expected=(
                f"'{self._MOUNT_POINT}' mounted separately (tmpfs or partition); "
                f"'{self._UNIT}' not masked or disabled"
            ),
            found=f"mounted={mounted}, {self._UNIT}_state={enabled_state}",
        )
