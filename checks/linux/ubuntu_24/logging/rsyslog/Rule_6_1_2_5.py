from core import Mode
from checks.templates.manual import ManualRule


class Rule_6_1_2_5(ManualRule):
    rule_id = "6.1.2.5"
    title = "Ensure rsyslog is configured to send logs to a remote log host"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
