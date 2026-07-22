from ._Base_6_2_2 import AuditdOptionRule


class Rule_6_2_2_2(AuditdOptionRule):
    rule_id = "6.2.2.2"
    title = "Ensure audit logs are not automatically deleted"
    workstation_lvl = 2
    server_lvl = 2
    _OPTION = "max_log_file_action"
    _ALLOWED = {"keep_logs"}
