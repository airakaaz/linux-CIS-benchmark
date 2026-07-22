from ._Base_5_4 import AccountPolicyRule, pass_warn_age


class Rule_5_4_1_3(AccountPolicyRule):
    rule_id = "5.4.1.3"
    title = "Ensure password expiration warning days is configured"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(pass_warn_age)
    _EXPECTED = "PASS_WARN_AGE >= 7 and password users have at least 7 days"
