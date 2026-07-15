from ._Base_5_4 import AccountPolicyRule, umask


class Rule_5_4_3_3(AccountPolicyRule):
    rule_id = "5.4.3.3"
    title = "Ensure default user umask is configured"
    _CHECK = staticmethod(umask)
    _EXPECTED = "profile umask and login UMASK are at least as restrictive as 0027"
