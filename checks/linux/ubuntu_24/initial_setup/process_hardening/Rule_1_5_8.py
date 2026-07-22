from ._Base_1_5 import KernelParamRule


class Rule_1_5_8(KernelParamRule):
    rule_id = "1.5.8"
    _PARAM = "kernel.kptr_restrict"
    _ALLOW = {"1", "2"}
    title = f"Ensure {_PARAM} is configured"
    server_lvl = 1
    workstation_lvl = 1
