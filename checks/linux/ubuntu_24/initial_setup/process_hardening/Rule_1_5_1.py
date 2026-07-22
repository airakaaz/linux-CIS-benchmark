from ._Base_1_5 import KernelParamRule


class Rule_1_5_1(KernelParamRule):
    rule_id = "1.5.1"
    _PARAM = "fs.protected_hardlinks"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
    server_lvl = 1
    workstation_lvl = 1
