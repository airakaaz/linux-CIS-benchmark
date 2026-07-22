from ._Base_5_1 import SshdOptionRule


class Rule_5_1_13(SshdOptionRule):
    rule_id = "5.1.13"
    title = "Ensure sshd LoginGraceTime is configured"
    workstation_lvl = 1
    server_lvl = 1
    _OPTION = "logingracetime"

    def is_compliant(self, value):
        try:
            return 1 <= int(value) <= 60
        except (TypeError, ValueError):
            return False

    def expected_value(self):
        return "logingracetime between 1 and 60 seconds"
