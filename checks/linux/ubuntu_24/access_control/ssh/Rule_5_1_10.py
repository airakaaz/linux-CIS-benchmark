from ._Base_5_1 import SshdOptionRule


class Rule_5_1_10(SshdOptionRule):
    rule_id = "5.1.10"
    title = "Ensure sshd HostbasedAuthentication is disabled"
    _OPTION = "hostbasedauthentication"

    def is_compliant(self, value):
        return value == "no"

    def expected_value(self):
        return "hostbasedauthentication no"
