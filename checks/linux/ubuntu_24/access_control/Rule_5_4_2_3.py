from ._Base_5_4 import AccountPolicyRule, only_root_gid_group


class Rule_5_4_2_3(AccountPolicyRule):
    rule_id = "5.4.2.3"
    title = "Ensure group root is the only GID 0 group"
    _CHECK = staticmethod(only_root_gid_group)
    _EXPECTED = "only root group has GID 0"
