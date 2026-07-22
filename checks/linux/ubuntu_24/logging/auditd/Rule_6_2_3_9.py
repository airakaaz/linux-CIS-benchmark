from pathlib import Path

from core import ScanResult
from ._Base_6_2_3 import AuditRuleSetRule, watch


class Rule_6_2_3_9(AuditRuleSetRule):
    rule_id = "6.2.3.9"
    title = "Ensure events that modify /etc/netplan are collected"
    workstation_lvl = 2
    server_lvl = 2

    _PATTERNS = (watch("/etc/netplan", "system-locale"),)

    def check(self) -> ScanResult:
        if not Path("/etc/netplan").exists():
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message="/etc/netplan does not exist; not applicable.",
                expected="/etc/netplan is watched if it exists",
                found="/etc/netplan not present",
            )
        return super().check()
