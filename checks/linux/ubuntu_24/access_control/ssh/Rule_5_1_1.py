from ._Base_5_1 import SshAccessRule
from utils import ssh


class Rule_5_1_1(SshAccessRule):
    rule_id = "5.1.1"
    title = "Ensure access to /etc/ssh/sshd_config is configured"
    workstation_lvl = 1
    server_lvl = 1

    def check(self):
        return self.access_result(
            ssh.config_files(),
            max_mode=0o600,
            expected="sshd_config and included .conf files are mode 0600 or more restrictive and owned by root:root",
        )
