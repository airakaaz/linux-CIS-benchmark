from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_10(KernelModuleRule):
    rule_id = "1.1.1.10"
    _MODULE = "usb-storage"
    _TYPE = "drivers"
    title = f"Ensure {_MODULE} kernel module is not available"
