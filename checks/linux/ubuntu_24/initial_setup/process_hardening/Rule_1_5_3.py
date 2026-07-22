from ._Base_1_5 import KernelParamRule


class Rule_1_5_3(KernelParamRule):
    rule_id = "1.5.3"
    _PARAM = "kernel.yama.ptrace_scope"
    _ALLOW = {"1", "2", "3"}
    _UFW_OVERRIDE_NOTE = True
    title = f"Ensure {_PARAM} is configured"
    server_lvl = 1
    workstation_lvl = 1
