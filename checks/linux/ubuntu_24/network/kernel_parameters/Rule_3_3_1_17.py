from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_17(KernelParamRule):
    rule_id = "3.3.1.17"
    _PARAM = "net.ipv4.conf.default.log_martians"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 1
    server_lvl = 1
