from core import ScanResult
from ._Base_5_1 import SshdOptionRule
from utils import ssh


class Rule_5_1_15(SshdOptionRule):
    rule_id = "5.1.15"
    title = "Ensure sshd MACs are configured"
    workstation_lvl = 1
    server_lvl = 1
    _OPTION = "macs"

    def check(self):
        value = self.option_value() or ""
        weak = ssh.weak_macs(value)
        passed = bool(value) and not weak
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="sshd MACs contain no weak MACs" if passed else "sshd MACs are missing or contain weak MACs",
            expected="no weak HMAC-MD5, HMAC-SHA1-96, UMAC-64, or weak ETM MACs", found=value or "not set",
        )
