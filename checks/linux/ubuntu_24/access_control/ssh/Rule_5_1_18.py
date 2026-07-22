from ._Base_5_1 import SshdOptionRule


class Rule_5_1_18(SshdOptionRule):
    rule_id = "5.1.18"
    title = "Ensure sshd MaxSessions is configured"
    workstation_lvl = 1
    server_lvl = 1
    _OPTION = "maxsessions"

    def is_compliant(self, value):
        try:
            return int(value) <= 10
        except (TypeError, ValueError):
            return False

    def expected_value(self):
        return "maxsessions <= 10"
