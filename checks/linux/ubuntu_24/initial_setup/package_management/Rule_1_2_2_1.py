from core import Mode
from checks.templates.manual import ManualRule


class Rule_1_2_2_1(ManualRule):
    rule_id = "1.2.2.1"
    title = "Ensure updates, patches, and additional security software are installed"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
