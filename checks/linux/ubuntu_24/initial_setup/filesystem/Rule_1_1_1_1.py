from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_1(KernelModuleRule):
    rule_id = "1.1.1.1"
    _MODULE = "cramfs"
    title = f"Ensure {_MODULE} kernel module is not available"
    server_lvl = 1
    workstation_lvl = 1
