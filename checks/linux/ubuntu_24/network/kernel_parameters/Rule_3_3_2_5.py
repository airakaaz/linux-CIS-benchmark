from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_2_5(KernelParamRule):
    rule_id = "3.3.2.5"
    _PARAM = "net.ipv6.conf.all.accept_source_route"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
