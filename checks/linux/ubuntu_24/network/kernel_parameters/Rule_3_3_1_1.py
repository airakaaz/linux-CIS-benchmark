from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_1(KernelParamRule):
    rule_id = "3.3.1.1"
    _PARAM = "net.ipv4.ip_forward"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 2
    server_lvl = 1
