from ._Base_5_4 import AccountPolicyRule, no_nologin_shell


class Rule_5_4_3_1(AccountPolicyRule):
    rule_id = "5.4.3.1"
    title = "Ensure nologin is not listed in /etc/shells"
    _CHECK = staticmethod(no_nologin_shell)
    _EXPECTED = "no /nologin shell is listed"
