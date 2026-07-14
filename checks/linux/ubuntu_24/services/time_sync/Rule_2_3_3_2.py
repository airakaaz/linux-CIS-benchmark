from core import CISRule, Mode, ScanResult

from ._Base_2_3 import chrony_is_active
from utils.command import run


class Rule_2_3_3_2(CISRule):
    rule_id = "2.3.3.2"
    title = "Ensure chrony is running as user _chrony"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        if not chrony_is_active():
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message="chrony is not in use; process user check not applicable",
                expected="chronyd runs as _chrony when chrony is in use",
                found="chrony.service is not active",
            )

        result = run("ps -eo user=,comm=")
        processes = [
            line.split(maxsplit=1)
            for line in result.stdout.splitlines()
            if len(line.split(maxsplit=1)) == 2 and line.split(maxsplit=1)[1] == "chronyd"
        ]
        passed = result.ok and bool(processes) and all(user == "_chrony" for user, _ in processes)
        found = ", ".join(f"{user} ({command})" for user, command in processes) or "chronyd process not found"

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "chronyd is running as _chrony"
                if passed
                else "chronyd is not running exclusively as _chrony"
            ),
            expected="all chronyd processes run as _chrony",
            found=found,
        )
