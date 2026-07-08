import re
from core import CISRule, Mode, ScanResult
from utils.command import run


class Rule_1_3_1_3(CISRule):
    rule_id = "1.3.1.3"
    title = "Ensure all AppArmor Profiles are enforcing"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        status = run("apparmor_status").stdout

        profiles = re.search(r"^\d profiles are loaded", status)
        processes = re.search(r"^\d processes have been defined", status)

        if profiles and processes:
            profiles_enforced = re.search(
                rf"^{profiles.group().split()[0]} profiles are in enforce mode", status
            )
            processes_enforced = re.search(
                rf"^{processes.group().split()[0]} processes are in enforce mode",
                status,
            )
        else:
            profiles_enforced = processes_enforced = False

        if profiles_enforced and processes_enforced:
            passed = True
            message = "all profiles and processes in enforce mode"
        else:
            passed = False
            message = "some profile(s) and/or processe(s) are not in enforce mode"

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
        )
