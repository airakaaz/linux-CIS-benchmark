from core import Mode
from checks.templates.manual import ManualRule


class Rule_6_1_1_1_4(ManualRule):
    rule_id = "6.1.1.1.4"
    title = "Ensure journald log file access is configured"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
