from ._Base_5_1 import SshdOptionRule


class Rule_5_1_16(SshdOptionRule):
    rule_id = "5.1.16"
    title = "Ensure sshd MaxAuthTries is configured"
    workstation_lvl = 1
    server_lvl = 1
    _OPTION = "maxauthtries"

    def is_compliant(self, value):
        try:
            return int(value) <= 4
        except (TypeError, ValueError):
            return False

    def expected_value(self):
        return "maxauthtries <= 4"
