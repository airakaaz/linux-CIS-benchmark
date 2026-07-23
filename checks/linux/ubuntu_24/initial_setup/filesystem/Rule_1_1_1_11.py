from core import Mode
from checks.templates.manual import ManualRule


class Rule_1_1_1_11(ManualRule):
    rule_id = "1.1.1.11"
    title = "Ensure unused filesystems kernel modules are not available"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
