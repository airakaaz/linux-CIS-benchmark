from core import Mode
from checks.templates.manual import ManualRule


class Rule_6_1_1_1_5(ManualRule):
    rule_id = "6.1.1.1.5"
    title = "Ensure journald log file rotation is configured"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
