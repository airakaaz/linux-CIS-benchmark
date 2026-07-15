from ._Base_5_1 import SshdOptionRule


class Rule_5_1_22(SshdOptionRule):
    rule_id = "5.1.22"
    title = "Ensure sshd UsePAM is enabled"
    _OPTION = "usepam"

    def is_compliant(self, value):
        return value == "yes"

    def expected_value(self):
        return "usepam yes"
