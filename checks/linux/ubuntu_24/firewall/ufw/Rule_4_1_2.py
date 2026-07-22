import re

from core import ScanResult
from utils.command import run

from checks.templates.service_status import EnabledServiceRule


class Rule_4_1_2(EnabledServiceRule):
    rule_id = "4.1.2"
    title = "Ensure ufw service is enabled and active"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK_ACTIVE = True

    def check(self) -> ScanResult:
        result = super().check()
        status = run("ufw status")

        status_ok = status.ok and re.search(
            r"^Status:\s*active\b", status.stdout, re.MULTILINE
        )
        passed = result.passed and bool(status_ok)

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "ufw service is enabled, active, and ufw reports active status"
                if passed
                else "ufw service is not fully enabled, active, or ufw is not active"
            ),
            expected="enabled, active, and Status: active",
            found=(f"{result.found}; ufw status={status.stdout.strip() or 'failed'}"),
        )
