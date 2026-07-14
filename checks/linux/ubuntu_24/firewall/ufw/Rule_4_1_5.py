from ._Base_4_1 import UfwDefaultPolicyRule


class Rule_4_1_5(UfwDefaultPolicyRule):
    rule_id = "4.1.5"
    title = "Ensure ufw routing default is configured"

    _FIELD_INDEX = 2
    _ALLOWED_PREFIXES = ("disabled", "deny")
