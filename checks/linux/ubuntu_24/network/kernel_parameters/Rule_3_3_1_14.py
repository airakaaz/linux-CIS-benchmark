from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_14(KernelParamRule):
    rule_id = "3.3.1.14"
    _PARAM = "net.ipv4.conf.all.accept_source_route"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 1
    server_lvl = 1
