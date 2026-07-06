from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_2(KernelModuleRule):
    rule_id = "1.1.1.2"
    _MODULE = "freevxfs"
    title = f"Ensure {_MODULE} kernel module is not available"
