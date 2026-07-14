from core import CISRule, Mode, ScanResult

from ._Base_2_3 import timesyncd_options


class Rule_2_3_2_1(CISRule):
    rule_id = "2.3.2.1"
    title = "Ensure systemd-timesyncd configured with authorized timeserver"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        options = timesyncd_options()
        configured = {name: value for name, value in options.items() if value[0]}
        passed = bool(configured)

        found = (
            "; ".join(
                f"{name}={value} ({path})"
                for name, (value, path) in configured.items()
            )
            if configured
            else "NTP and FallbackNTP are not set"
        )
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "at least one timeserver option is configured"
                if passed
                else "neither NTP nor FallbackNTP is configured"
            ),
            expected="NTP and/or FallbackNTP set to site-approved authoritative timeserver(s)",
            found=found,
        )
