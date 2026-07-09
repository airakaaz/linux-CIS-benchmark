from ._Base_3_2 import KernelModuleRule


class Rule_3_2_2(KernelModuleRule):
    rule_id = "3_2_2"
    _MODULE = "can"
    title = f"Ensure {_MODULE} kernel module is not available"
