from core import ScanResult
from ._Base_5_1 import SshAccessRule
from utils import ssh


class Rule_5_1_6(SshAccessRule):
    rule_id = "5.1.6"
    title = "Ensure sshd Ciphers are configured"
    workstation_lvl = 1
    server_lvl = 1

    def check(self):
        options = ssh.effective_options()
        values = options.get("ciphers", [])
        ciphers = values[-1] if values else ""
        weak = ssh.weak_ciphers(ciphers)
        passed = bool(ciphers) and not weak
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="sshd ciphers are configured without weak ciphers" if passed else "sshd ciphers are missing or include weak ciphers",
            expected="sshd ciphers contain none of the weak CBC, 3DES, Blowfish, CAST, arcfour, or rijndael ciphers",
            found=ciphers or "none",
        )
