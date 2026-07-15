from ._Base_5_4 import AccountPolicyRule, root_password


class Rule_5_4_2_4(AccountPolicyRule):
    rule_id = "5.4.2.4"
    title = "Ensure root account access is controlled"
    _CHECK = staticmethod(root_password)
    _EXPECTED = "root password status is P or L"
