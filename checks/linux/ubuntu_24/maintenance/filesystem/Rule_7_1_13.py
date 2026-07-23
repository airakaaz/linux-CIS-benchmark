from core import Mode
from checks.templates.manual import ManualRule


class Rule_7_1_13(ManualRule):
    rule_id = "7.1.13"
    title = "Ensure SUID and SGID files are reviewed"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
