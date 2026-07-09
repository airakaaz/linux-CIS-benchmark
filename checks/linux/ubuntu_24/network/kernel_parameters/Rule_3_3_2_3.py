from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_2_3(KernelParamRule):
    rule_id = "3.3.2.3"
    _PARAM = "net.ipv6.conf.all.accept_redirects"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
