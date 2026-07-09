from ._Base_1_5 import KernelParamRule


class Rule_1_5_4(KernelParamRule):
    rule_id = "1.5.4"
    _PARAM = "kernel.dmesg_restrict"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
