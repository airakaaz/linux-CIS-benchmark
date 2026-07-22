from ._Base_5_1 import SshdOptionRule


class Rule_5_1_9(SshdOptionRule):
    rule_id = "5.1.9"
    title = "Ensure sshd GSSAPIAuthentication is disabled"
    workstation_lvl = 2
    server_lvl = 1
    _OPTION = "gssapiauthentication"

    def is_compliant(self, value):
        return value == "no"

    def expected_value(self):
        return "gssapiauthentication no"
