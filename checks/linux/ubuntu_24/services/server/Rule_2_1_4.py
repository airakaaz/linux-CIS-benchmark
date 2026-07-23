from core import Mode
from checks.templates.manual import ManualRule


class Rule_2_1_4(ManualRule):
    rule_id = "2.1.4"
    title = "Ensure only approved services are listening on a network interface"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
