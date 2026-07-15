from ._Base_5_1 import SshdOptionRule


class Rule_5_1_14(SshdOptionRule):
    rule_id = "5.1.14"
    title = "Ensure sshd LogLevel is configured"
    _OPTION = "loglevel"

    def is_compliant(self, value):
        return value in {"INFO", "VERBOSE"}

    def expected_value(self):
        return "loglevel INFO or VERBOSE"
