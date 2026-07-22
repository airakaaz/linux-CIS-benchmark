from ._Base_6_2_2 import AuditdOptionRule


class Rule_6_2_2_1(AuditdOptionRule):
    rule_id = "6.2.2.1"
    title = "Ensure audit log storage size is configured"
    workstation_lvl = 2
    server_lvl = 2
    _OPTION = "max_log_file"

    def is_compliant(self, value):
        try:
            return int(value) > 0
        except (TypeError, ValueError):
            return False

    def expected_value(self):
        return "max_log_file is a positive number of megabytes"
