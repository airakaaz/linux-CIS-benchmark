from ._Base_5_1 import SshAccessRule
from utils import ssh


class Rule_5_1_2(SshAccessRule):
    rule_id = "5.1.2"
    title = "Ensure access to SSH private host key files is configured"
    workstation_lvl = 1
    server_lvl = 1

    def check(self):
        return self.access_result(
            ssh.private_host_keys(),
            max_mode=0o600,
            expected="SSH private host key files are mode 0600 or more restrictive and owned by root:root",
        )
