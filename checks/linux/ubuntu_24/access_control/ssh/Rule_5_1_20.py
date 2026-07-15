from ._Base_5_1 import SshdOptionRule


class Rule_5_1_20(SshdOptionRule):
    rule_id = "5.1.20"
    title = "Ensure sshd PermitRootLogin is disabled"
    _OPTION = "permitrootlogin"

    def is_compliant(self, value):
        return value == "no"

    def expected_value(self):
        return "permitrootlogin no"
