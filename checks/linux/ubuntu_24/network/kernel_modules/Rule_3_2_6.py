from ._Base_3_2 import KernelModuleRule


class Rule_3_2_6(KernelModuleRule):
    rule_id = "3_2_6"
    _MODULE = "tipc"
    title = f"Ensure {_MODULE} kernel module is not available"
