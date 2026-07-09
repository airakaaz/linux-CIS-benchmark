from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_2_8(KernelParamRule):
    rule_id = "3.3.2.8"
    _PARAM = "net.ipv6.conf.default.accept_ra"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
