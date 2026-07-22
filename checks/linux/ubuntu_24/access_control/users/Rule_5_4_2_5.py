from ._Base_5_4 import AccountPolicyRule, root_path


class Rule_5_4_2_5(AccountPolicyRule):
    rule_id = "5.4.2.5"
    title = "Ensure root path integrity"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(root_path)
    _EXPECTED = (
        "root PATH contains only root-owned directories with restrictive permissions"
    )
