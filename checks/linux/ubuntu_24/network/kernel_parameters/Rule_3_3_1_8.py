from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_8(KernelParamRule):
    rule_id = "3.3.1.8"
    _PARAM = "net.ipv4.conf.all.accept_redirects"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
