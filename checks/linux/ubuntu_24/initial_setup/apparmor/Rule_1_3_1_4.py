from checks.templates.kernel_parameter import KernelParamRule


class Rule_1_3_1_4(KernelParamRule):
    rule_id = "1.3.1.4"
    _PARAM = "kernel.apparmor_restrict_unprivileged_unconfined"
    _ALLOW = {"1"}
    _UFW_OVERRIDE_NOTE = True
    title = f"Ensure {_PARAM} is enabled"
