from ._Base_5_4 import AccountPolicyRule, only_root_uid


class Rule_5_4_2_1(AccountPolicyRule):
    rule_id = "5.4.2.1"
    title = "Ensure root is the only UID 0 account"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(only_root_uid)
    _EXPECTED = "only root has UID 0"
