from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_3(KernelModuleRule):
    rule_id = "1.1.1.3"
    _MODULE = "hfs"
    title = f"Ensure {_MODULE} kernel module is not available"
