from ._Base_1_5 import KernelParamRule


class Rule_1_5_9(KernelParamRule):
    rule_id = "1.5.9"
    _PARAM = "kernel.randomize_va_space"
    _ALLOW = {"2"}
    title = f"Ensure {_PARAM} is configured"
