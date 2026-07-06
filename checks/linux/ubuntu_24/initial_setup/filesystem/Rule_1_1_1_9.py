from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_9(KernelModuleRule):
    rule_id = "1.1.1.9"
    _MODULE = "firewire-core"
    title = f"Ensure {_MODULE} kernel module is not available"
