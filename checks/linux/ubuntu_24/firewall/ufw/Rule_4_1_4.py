from ._Base_4_1 import UfwDefaultPolicyRule


class Rule_4_1_4(UfwDefaultPolicyRule):
    rule_id = "4.1.4"
    title = "Ensure ufw outgoing default is configured"

    _FIELD_INDEX = 1
    _ALLOWED_PREFIXES = ("deny", "reject")
