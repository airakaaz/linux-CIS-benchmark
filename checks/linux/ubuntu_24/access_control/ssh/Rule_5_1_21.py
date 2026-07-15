from ._Base_5_1 import SshdOptionRule


class Rule_5_1_21(SshdOptionRule):
    rule_id = "5.1.21"
    title = "Ensure sshd PermitUserEnvironment is disabled"
    _OPTION = "permituserenvironment"

    def is_compliant(self, value):
        return value == "no"

    def expected_value(self):
        return "permituserenvironment no"
