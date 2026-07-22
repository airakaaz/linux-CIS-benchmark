from core import CISRule, Mode, ScanResult
from utils import sudo


class Rule_5_2_6(CISRule):
    rule_id = "5.2.6"
    title = "Ensure sudo timestamp_timeout is configured"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        values = sudo.timestamp_values()
        if not values:
            default = sudo.default_timestamp_timeout()
            values = [] if default is None else [default]
        passed = bool(values) and all(0 <= value <= 15 for value in values)
        found = ", ".join(str(value) for value in values) if values else "not available"
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="sudo timestamp timeout is within the permitted range" if passed else "sudo timestamp timeout is missing, disabled, or exceeds 15 minutes",
            expected="timestamp_timeout is not negative and is no greater than 15 minutes",
            found=found,
        )
