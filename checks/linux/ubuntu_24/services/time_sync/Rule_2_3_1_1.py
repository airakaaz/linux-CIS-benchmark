from core import CISRule, Mode, ScanResult
from utils.command import run


class Rule_2_3_1_1(CISRule):
    rule_id = "2.3.1.1"
    title = "Ensure a single time synchronization daemon is in use"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    _SERVICES = ("systemd-timesyncd.service", "chrony.service")

    @staticmethod
    def _service_is_enabled(service: str) -> bool:
        result = run(f"systemctl is-enabled {service}")
        return result.ok and "enabled" in result.stdout

    @staticmethod
    def _service_is_active(service: str) -> bool:
        result = run(f"systemctl is-active {service}")
        return result.ok and result.stdout.strip().startswith("active")

    def check(self) -> ScanResult:
        enabled: list[str] = []
        active: list[str] = []

        for service in self._SERVICES:
            if self._service_is_enabled(service):
                enabled.append(service)
            if self._service_is_active(service):
                active.append(service)

        in_use = sorted(set(enabled) | set(active))
        passed = len(in_use) == 1

        if passed:
            message = f'Single time sync daemon in use: "{in_use[0]}"'
        elif not in_use:
            message = "No time sync daemon is in use on the system"
        else:
            message = f"More than one time sync daemon is in use: {', '.join(in_use)}"

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
            expected="exactly one of systemd-timesyncd.service or chrony.service enabled or active",
            found=", ".join(in_use) if in_use else "none",
        )
