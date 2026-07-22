from core import ScanResult
from ._Base_5_1 import SshdOptionRule
from utils import ssh


class Rule_5_1_24(SshdOptionRule):
    rule_id = "5.1.24"
    title = "Ensure sshd ListenAddress is configured"
    workstation_lvl = 2
    server_lvl = 2
    _OPTION = "listenaddress"

    def check(self):
        values = ssh.effective_options().get(self._OPTION, [])
        private = ssh.private_listen_addresses(values)
        passed = bool(private)
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="sshd ListenAddress includes a private network interface" if passed else "sshd ListenAddress does not include a private network interface",
            expected="at least one ListenAddress uses a non-loopback private IP address",
            found=", ".join(values) if values else "not set",
        )
