from core import CISRule, Mode, ScanResult
from utils import sudo


class Rule_5_2_2(CISRule):
    rule_id = "5.2.2"
    title = "Ensure sudo commands use pty"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        enabled = sudo.active_lines(r"^\s*Defaults\s+(?:[^#]*,\s*)?use_pty\b")
        disabled = sudo.active_lines(r"^\s*Defaults\s+(?:[^#]*,\s*)?!use_pty\b")
        passed = bool(enabled) and not disabled
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="sudo use_pty is enabled" if passed else "sudo use_pty is missing or disabled",
            expected="Defaults use_pty and no active Defaults !use_pty",
            found=f"enabled={len(enabled)}, disabled={len(disabled)}",
        )
