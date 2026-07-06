from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_4(KernelModuleRule):
    rule_id = "1.1.1.4"
    _MODULE = "hfsplus"
    title = f"Ensure {_MODULE} kernel module is not available"
