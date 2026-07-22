from core import ScanResult
from ._Base_5_1 import SshdOptionRule
from utils import ssh


class Rule_5_1_12(SshdOptionRule):
    rule_id = "5.1.12"
    title = "Ensure sshd KexAlgorithms are configured"
    workstation_lvl = 1
    server_lvl = 1
    _OPTION = "kexalgorithms"

    def check(self):
        value = self.option_value() or ""
        weak = ssh.weak_kex_algorithms(value)
        passed = bool(value) and not weak
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="sshd KexAlgorithms contain no weak algorithms" if passed else "sshd KexAlgorithms are missing or contain weak algorithms",
            expected="no diffie-hellman SHA-1 KexAlgorithms", found=value or "not set",
        )
