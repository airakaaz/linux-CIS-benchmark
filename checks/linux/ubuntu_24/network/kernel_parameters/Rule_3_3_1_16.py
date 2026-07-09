from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_16(KernelParamRule):
    rule_id = "3.3.1.16"
    _PARAM = "net.ipv4.conf.all.log_martians"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
