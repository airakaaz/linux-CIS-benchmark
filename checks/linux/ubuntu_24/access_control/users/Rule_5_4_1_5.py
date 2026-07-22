from ._Base_5_4 import AccountPolicyRule, inactive_days


class Rule_5_4_1_5(AccountPolicyRule):
    rule_id = "5.4.1.5"
    title = "Ensure inactive password lock is configured"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(inactive_days)
    _EXPECTED = "INACTIVE is 0..45 and password users have 0..45 days"
