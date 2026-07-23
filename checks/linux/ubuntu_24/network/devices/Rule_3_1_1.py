from core import Mode
from checks.templates.manual import ManualRule


class Rule_3_1_1(ManualRule):
    rule_id = "3.1.1"
    title = "Ensure IPv6 status is identified"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
