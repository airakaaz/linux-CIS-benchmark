from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_2(KernelParamRule):
    rule_id = "3.3.1.2"
    _PARAM = "net.ipv4.conf.all.forwarding"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
