from core import Mode
from checks.templates.manual import ManualRule


class Rule_6_1_2_10(ManualRule):
    rule_id = "6.1.2.10"
    title = "Ensure rsyslog CA certificates are configured"
    server_lvl = 2
    workstation_lvl = 2
    mode = Mode.MANUAL
