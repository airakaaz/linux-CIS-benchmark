from ._Base_5_1 import SshdOptionRule


class Rule_5_1_19(SshdOptionRule):
    rule_id = "5.1.19"
    title = "Ensure sshd PermitEmptyPasswords is disabled"
    workstation_lvl = 1
    server_lvl = 1
    _OPTION = "permitemptypasswords"

    def is_compliant(self, value):
        return value == "no"

    def expected_value(self):
        return "permitemptypasswords no"
