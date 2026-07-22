from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_2_2(KernelParamRule):
    rule_id = "3.3.2.2"
    _PARAM = "net.ipv6.conf.default.forwarding"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 1
    server_lvl = 1
