from ._Base_1_1_1 import KernelModuleRule


class Rule_1_1_1_6(KernelModuleRule):
    rule_id = "1.1.1.6"
    _MODULE = "overlayfs"
    title = "Ensure overlay kernel module is not available"
    server_lvl = 2
    workstation_lvl = 2
