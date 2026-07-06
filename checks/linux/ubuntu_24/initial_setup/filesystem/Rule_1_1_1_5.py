from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_5(KernelModuleRule):
    rule_id = "1.1.1.5"
    _MODULE = "jffs2"
    title = f"Ensure {_MODULE} kernel module is not available"
