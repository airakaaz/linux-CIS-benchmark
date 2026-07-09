from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_2_6(KernelParamRule):
    rule_id = "3.3.2.6"
    _PARAM = "net.ipv6.conf.default.accept_source_route"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
