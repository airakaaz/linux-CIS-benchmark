from core import Mode
from checks.templates.manual import ManualRule


class Rule_5_4_1_2(ManualRule):
    rule_id = "5.4.1.2"
    title = "Ensure minimum password days is configured"
    server_lvl = 2
    workstation_lvl = 2
    mode = Mode.MANUAL
