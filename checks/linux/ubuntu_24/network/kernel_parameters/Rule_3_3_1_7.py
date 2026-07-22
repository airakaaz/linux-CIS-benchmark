from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_7(KernelParamRule):
    rule_id = "3.3.1.7"
    _PARAM = "net.ipv4.icmp_echo_ignore_broadcasts"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 1
    server_lvl = 1
