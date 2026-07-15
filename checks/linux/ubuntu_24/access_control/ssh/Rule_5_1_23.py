from core import ScanResult
from ._Base_5_1 import SshdOptionRule
from utils import ssh


class Rule_5_1_23(SshdOptionRule):
    rule_id = "5.1.23"
    title = "Ensure sshd post-quantum cryptography key exchange algorithms are configured"
    _OPTION = "kexalgorithms"

    def check(self):
        value = self.option_value() or ""
        version = ssh.openssh_version()
        required = ["sntrup761x25519-sha512"]
        if version is not None and version >= (9, 9):
            required.append("mlkem768x25519-sha256")
        passed = bool(version) and all(algorithm in value.split(",") for algorithm in required)
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="required post-quantum KEX algorithms are available" if passed else "required post-quantum KEX algorithms are not available",
            expected=f"OpenSSH version detected and KexAlgorithms includes {', '.join(required)}",
            found=f"version={version}, kexalgorithms={value or 'not set'}",
        )
