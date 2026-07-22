from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_8(KernelModuleRule):
    rule_id = "1.1.1.8"
    _MODULE = "udf"
    title = f"Ensure {_MODULE} kernel module is not available"
    server_lvl = 2
    workstation_lvl = 2
