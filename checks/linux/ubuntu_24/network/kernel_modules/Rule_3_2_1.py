from ._Base_3_2 import KernelModuleRule


class Rule_3_2_1(KernelModuleRule):
    rule_id = "3_2_1"
    _MODULE = "atm"
    _TYPE = "net"
    title = f"Ensure {_MODULE} kernel module is not available"
    workstation_lvl = 1
    server_lvl = 1
