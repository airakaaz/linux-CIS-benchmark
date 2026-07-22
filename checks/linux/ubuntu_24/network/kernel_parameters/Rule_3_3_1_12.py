from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_12(KernelParamRule):
    rule_id = "3.3.1.12"
    _PARAM = "net.ipv4.conf.all.rp_filter"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 1
    server_lvl = 1
