from checks.templates.systemd_conf import SystemdConfOptionRule
from core import ScanResult
from utils import package, systemctl


class Rule_6_1_1_1_3(SystemdConfOptionRule):
    rule_id = "6.1.1.1.3"
    title = "Ensure journald is configured to send logs to rsyslog"
    workstation_lvl = 1
    server_lvl = 1
    _CONF_UNIT = "systemd/journald.conf"
    _SECTION = "Journal"
    _OPTION = "ForwardToSyslog"
    _ALLOW = {"yes"}
    _REQUIRED_PACKAGE = "rsyslog"

    _SERVICES = (
        "systemd-journald.service",
        "rsyslog.service",
    )

    def check(self) -> ScanResult:
        # The CIS rule is conditional on rsyslog being the selected logging
        # backend.  Keep the existing not-applicable result when it is not
        # installed.
        if package.not_installed(self._REQUIRED_PACKAGE).valid:
            return super().check()

        config_result = super().check()
        inactive = [
            service for service in self._SERVICES if not systemctl.is_active(service)
        ]

        issues = []
        if not config_result.passed:
            issues.append(config_result.message)
        if inactive:
            issues.append(
                "inactive services: " + ", ".join(inactive)
            )

        passed = not issues
        found = config_result.found or "configuration not found"
        if inactive:
            found += "; " + "; ".join(
                f"{service} is not active" for service in inactive
            )

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "ForwardToSyslog is set to yes and journald/rsyslog services are active."
                if passed
                else "; ".join(issues)
            ),
            expected=(
                "ForwardToSyslog=yes; systemd-journald.service and "
                "rsyslog.service are loaded and active"
            ),
            found=found,
        )
