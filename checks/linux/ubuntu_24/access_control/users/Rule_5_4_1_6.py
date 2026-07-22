from ._Base_5_4 import AccountPolicyRule, future_changes


class Rule_5_4_1_6(AccountPolicyRule):
    rule_id = "5.4.1.6"
    title = "Ensure all users last password change date is in the past"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(future_changes)
    _EXPECTED = "password change dates are not in the future"
