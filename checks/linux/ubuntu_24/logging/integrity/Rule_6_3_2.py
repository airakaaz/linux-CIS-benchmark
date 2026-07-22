from core import CISRule, Mode, ScanResult
from utils import systemctl


class Rule_6_3_2(CISRule):
    rule_id = "6.3.2"
    title = "Ensure filesystem integrity is regularly checked"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        timer_state = systemctl.get_enabled_state("dailyaidecheck.timer")
        service_state = systemctl.get_enabled_state("dailyaidecheck.service")
        active = systemctl.is_active("dailyaidecheck.timer")
        passed = timer_state == "enabled" and service_state in {"static", "enabled"} and active
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "dailyaidecheck timer is enabled and active"
                if passed
                else "dailyaidecheck timer/service is not configured correctly"
            ),
            expected="dailyaidecheck.timer enabled and active; dailyaidecheck.service static or enabled",
            found=f"service={service_state or 'unknown'}, timer={timer_state or 'unknown'}, active={active}",
        )
