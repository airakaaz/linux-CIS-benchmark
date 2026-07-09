from ._Base_1_5 import KernelParamRule


class Rule_1_5_4(KernelParamRule):
    rule_id = "1.5.4"
    _PARAM = "fs.suid_dumpable"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
