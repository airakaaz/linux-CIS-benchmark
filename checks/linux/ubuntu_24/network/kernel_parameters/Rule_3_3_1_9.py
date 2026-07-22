from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_9(KernelParamRule):
    rule_id = "3.3.1.9"
    _PARAM = "net.ipv4.conf.default.accept_redirects"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 1
    server_lvl = 1
