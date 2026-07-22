from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_10(KernelParamRule):
    rule_id = "3.3.1.10"
    _PARAM = "net.ipv4.conf.all.secure_redirects"
    _ALLOW = {"0"}
    title = f"Ensure {_PARAM} is configured"
    workstation_lvl = 1
    server_lvl = 1
