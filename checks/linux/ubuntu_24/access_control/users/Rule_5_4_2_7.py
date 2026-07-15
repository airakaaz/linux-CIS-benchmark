from ._Base_5_4 import AccountPolicyRule, system_shells


class Rule_5_4_2_7(AccountPolicyRule):
    rule_id = "5.4.2.7"
    title = "Ensure system accounts do not have a valid login shell"
    _CHECK = staticmethod(system_shells)
    _EXPECTED = "system accounts have no valid login shell"
