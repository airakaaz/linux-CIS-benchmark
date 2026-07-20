from ._Base_3_2 import KernelModuleRule


class Rule_3_2_5(KernelModuleRule):
    rule_id = "3_2_5"
    _MODULE = "sctp"
    _TYPE = "net"
    title = f"Ensure {_MODULE} kernel module is not available"
