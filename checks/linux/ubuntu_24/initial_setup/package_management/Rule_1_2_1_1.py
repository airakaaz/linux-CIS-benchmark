from core import Mode
from checks.templates.manual import ManualRule


class Rule_1_2_1_1(ManualRule):
    rule_id = "1.2.1.1"
    title = "Ensure the source.list and .source files use the Signed-By option"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.MANUAL
