from ._Base_5_4 import AccountPolicyRule, tmout


class Rule_5_4_3_2(AccountPolicyRule):
    rule_id = "5.4.3.2"
    title = "Ensure default user shell timeout is configured"
    _CHECK = staticmethod(tmout)
    _EXPECTED = "TMOUT is 1..900, readonly, and exported"
