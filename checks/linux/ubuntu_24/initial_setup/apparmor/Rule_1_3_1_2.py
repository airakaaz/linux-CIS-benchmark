from core import CISRule, Mode, ScanResult
from utils import grub


class Rule_1_3_1_2(CISRule):
    rule_id = "1.3.1.2"
    title = "Ensure AppArmor is enabled"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        passed = not grub.kernel_cmdline_has("apparmor=0")
        message = "AppArmor is " + "not disabled" if passed else "disabled"

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
        )
