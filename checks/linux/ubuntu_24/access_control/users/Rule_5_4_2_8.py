from ._Base_5_4 import AccountPolicyRule, locked_invalid_shells


class Rule_5_4_2_8(AccountPolicyRule):
    rule_id = "5.4.2.8"
    title = "Ensure accounts without a valid login shell are locked"
    _CHECK = staticmethod(locked_invalid_shells)
    _EXPECTED = "non-root accounts without valid shells are locked"
