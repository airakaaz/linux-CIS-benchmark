from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_18(KernelParamRule):
    rule_id = "3.3.1.18"
    _PARAM = "net.ipv4.tcp_syncookies"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
