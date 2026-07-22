from core import ScanResult
from ._Base_5_1 import SshAccessRule
from utils import ssh


class Rule_5_1_4(SshAccessRule):
    rule_id = "5.1.4"
    title = "Ensure sshd access is configured"
    workstation_lvl = 1
    server_lvl = 1

    def check(self):
        options = ssh.effective_options()
        access = {
            key: values
            for key, values in options.items()
            if key in {"allowusers", "allowgroups", "denyusers", "denygroups"}
            and any(value and value.lower() != "none" for value in values)
        }
        found = "; ".join(f"{key} {', '.join(values)}" for key, values in access.items())
        passed = bool(access)
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="sshd access restrictions are configured" if passed else "No sshd allow/deny access restriction is configured",
            expected="at least one of AllowUsers, AllowGroups, DenyUsers, or DenyGroups is configured",
            found=found or "none",
        )
