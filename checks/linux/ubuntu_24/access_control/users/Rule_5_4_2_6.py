from ._Base_5_4 import AccountPolicyRule, root_umask


class Rule_5_4_2_6(AccountPolicyRule):
    rule_id = "5.4.2.6"
    title = "Ensure root user umask is configured"
    _CHECK = staticmethod(root_umask)
    _EXPECTED = "root umask is at least as restrictive as 0027"
