from ._Base_5_1 import SshdOptionRule


class Rule_5_1_17(SshdOptionRule):
    rule_id = "5.1.17"
    title = "Ensure sshd MaxStartups is configured"
    workstation_lvl = 1
    server_lvl = 1
    _OPTION = "maxstartups"

    def is_compliant(self, value):
        try:
            start, rate, full = (int(part) for part in value.split(":", 2))
            return start <= 10 and rate <= 30 and full <= 60
        except (AttributeError, TypeError, ValueError):
            return False

    def expected_value(self):
        return "maxstartups <= 10:30:60"
