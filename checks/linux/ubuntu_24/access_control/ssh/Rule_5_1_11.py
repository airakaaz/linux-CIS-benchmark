from ._Base_5_1 import SshdOptionRule


class Rule_5_1_11(SshdOptionRule):
    rule_id = "5.1.11"
    title = "Ensure sshd IgnoreRhosts is enabled"
    workstation_lvl = 1
    server_lvl = 1
    _OPTION = "ignorerhosts"

    def is_compliant(self, value):
        return value == "yes"

    def expected_value(self):
        return "ignorerhosts yes"
