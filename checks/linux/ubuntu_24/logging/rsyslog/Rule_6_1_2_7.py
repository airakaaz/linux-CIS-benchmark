from core import Mode
from checks.templates.manual import ManualRule


class Rule_6_1_2_7(ManualRule):
    rule_id = "6.1.2.7"
    title = "Ensure logrotate is configured"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
