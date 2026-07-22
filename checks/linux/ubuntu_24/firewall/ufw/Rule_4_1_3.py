from ._Base_4_1 import UfwDefaultPolicyRule


class Rule_4_1_3(UfwDefaultPolicyRule):
    rule_id = "4.1.3"
    title = "Ensure ufw incoming default is configured"
    workstation_lvl = 1
    server_lvl = 1

    _FIELD_INDEX = 0
    _ALLOWED_PREFIXES = ("deny", "reject")
