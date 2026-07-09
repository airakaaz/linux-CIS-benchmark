from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_15(KernelParamRule):
    rule_id = "3.3.1.15"
    _PARAM = "net.ipv4.conf.default.accept_source_route"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
