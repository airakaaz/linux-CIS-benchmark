from core import Mode
from checks.templates.manual import ManualRule


class Rule_6_2_3_30(ManualRule):
    rule_id = "6.2.3.30"
    title = "Ensure the running and on disk configuration is the same"
    server_lvl = 2
    workstation_lvl = 2
    mode = Mode.MANUAL
