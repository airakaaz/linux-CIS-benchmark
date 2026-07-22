from ._Base_5_4 import AccountPolicyRule, only_root_gid_user


class Rule_5_4_2_2(AccountPolicyRule):
    rule_id = "5.4.2.2"
    title = "Ensure root is the only GID 0 account"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(only_root_gid_user)
    _EXPECTED = "only root has primary GID 0, excluding approved system users"
