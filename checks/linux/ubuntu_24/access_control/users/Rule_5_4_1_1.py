from ._Base_5_4 import AccountPolicyRule, pass_max_days


class Rule_5_4_1_1(AccountPolicyRule):
    rule_id = "5.4.1.1"
    title = "Ensure password expiration is configured"
    _CHECK = staticmethod(pass_max_days)
    _EXPECTED = "PASS_MAX_DAYS <= 365 and password users have 1..365 days"
