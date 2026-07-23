from core import Mode
from checks.templates.manual import ManualRule


class Rule_5_3_3_2_3(ManualRule):
    rule_id = "5.3.3.2.3"
    title = "Ensure password complexity is configured"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
