from checks.templates.kernel_parameter import KernelParamRule


class Rule_3_3_1_6(KernelParamRule):
    rule_id = "3.3.1.6"
    _PARAM = "net.ipv4.icmp_ignore_bogus_error_responses"
    _ALLOW = {"1"}
    title = f"Ensure {_PARAM} is configured"
