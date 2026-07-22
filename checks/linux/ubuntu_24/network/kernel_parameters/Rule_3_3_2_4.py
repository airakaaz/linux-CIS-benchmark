from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_2_4(KernelParamRule):
    rule_id = "3.3.2.4"
    _PARAM = "net.ipv6.conf.default.accept_redirects"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 1
    server_lvl = 1
