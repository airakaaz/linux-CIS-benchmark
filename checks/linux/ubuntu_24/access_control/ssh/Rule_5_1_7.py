from core import ScanResult
from ._Base_5_1 import SshAccessRule
from utils import ssh


class Rule_5_1_7(SshAccessRule):
    rule_id = "5.1.7"
    title = "Ensure sshd ClientAliveInterval and ClientAliveCountMax are configured"

    def check(self):
        options = ssh.effective_options()
        values = {}
        for option in ("clientaliveinterval", "clientalivecountmax"):
            raw = options.get(option, [""])[-1]
            try:
                values[option] = int(raw)
            except ValueError:
                values[option] = None

        passed = all(value is not None and value > 0 for value in values.values())
        found = "; ".join(f"{key}={value}" for key, value in values.items())
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="ClientAliveInterval and ClientAliveCountMax are greater than zero" if passed else "ClientAliveInterval and/or ClientAliveCountMax is not greater than zero",
            expected="ClientAliveInterval > 0 and ClientAliveCountMax > 0",
            found=found,
        )
