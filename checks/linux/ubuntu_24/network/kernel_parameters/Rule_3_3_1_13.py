from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_13(KernelParamRule):
    rule_id = "3.3.1.13"
    _PARAM = "net.ipv4.conf.default.rp_filter"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
