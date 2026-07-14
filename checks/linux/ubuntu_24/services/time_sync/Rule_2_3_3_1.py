from core import CISRule, Mode, ScanResult

from ._Base_2_3 import chrony_is_active, chrony_servers


class Rule_2_3_3_1(CISRule):
    rule_id = "2.3.3.1"
    title = "Ensure chrony is configured"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        if not chrony_is_active():
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message="chrony is not in use; configuration check not applicable",
                expected="server or pool directive when chrony is in use",
                found="chrony.service is not active",
            )

        servers = chrony_servers()
        passed = bool(servers)
        found = (
            "; ".join(f"{directive} ({path})" for path, directive in servers)
            if servers
            else "no server or pool directive found"
        )
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "chrony has an authorized-timeserver directive"
                if passed
                else "chrony has no server or pool directive"
            ),
            expected="server or pool directive in chrony configuration",
            found=found,
        )
