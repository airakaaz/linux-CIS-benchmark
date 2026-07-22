from ._Base_5_1 import SshAccessRule
from utils import ssh


class Rule_5_1_3(SshAccessRule):
    rule_id = "5.1.3"
    title = "Ensure access to SSH public host key files is configured"
    workstation_lvl = 1
    server_lvl = 1

    def check(self):
        return self.access_result(
            ssh.public_host_keys(),
            max_mode=0o644,
            expected="SSH public host key files are mode 0644 or more restrictive and owned by root:root",
        )
