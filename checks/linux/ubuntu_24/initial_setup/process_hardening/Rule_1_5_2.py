from ._Base_1_5 import KernelParamRule


class Rule_1_5_2(KernelParamRule):
    rule_id = "1.5.2"
    _PARAM = "fs.protected_symlinks"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
