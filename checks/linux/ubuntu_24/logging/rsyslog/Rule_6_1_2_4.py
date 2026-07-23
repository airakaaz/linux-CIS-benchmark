from core import Mode
from checks.templates.manual import ManualRule


class Rule_6_1_2_4(ManualRule):
    rule_id = "6.1.2.4"
    title = "Ensure rsyslog logging is configured"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
