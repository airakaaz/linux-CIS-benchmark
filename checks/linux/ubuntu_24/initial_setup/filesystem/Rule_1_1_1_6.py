from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_6(KernelModuleRule):
    rule_id = "1.1.1.6"
    _MODULE = "overlay"
    title = f"Ensure {_MODULE} kernel module is not available"
