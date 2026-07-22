from ._Base_5_1 import SshdOptionRule


class Rule_5_1_8(SshdOptionRule):
    rule_id = "5.1.8"
    title = "Ensure sshd DisableForwarding is enabled"
    workstation_lvl = 2
    server_lvl = 1
    _OPTION = "disableforwarding"

    def is_compliant(self, value):
        return value == "yes"

    def expected_value(self):
        return "disableforwarding yes"
