from core import ScanResult
from ._Base_6_2_3 import AuditRuleSetRule, executable
from utils import kernel_utils


class Rule_6_2_3_28(AuditRuleSetRule):
    rule_id = "6.2.3.28"
    title = "Ensure kernel module loading unloading and modification is collected"
    _PATTERNS = tuple(
        f"(?=.*arch={arch})(?=.*(?:init_module|finit_module|delete_module|create_module|query_module))(?=.*auid!=(?:unset|-1|4294967295))(?=.*(?:key=kernel_modules|-k\\s+kernel_modules))"
        for arch in ("b64", "b32")
    ) + (executable("/usr/bin/kmod", "kernel_modules"),)

    def check(self) -> ScanResult:
        result = super().check()
        if not kernel_utils.module_symlinks_point_to_kmod():
            result.passed = False
            result.message += "; kmod symlinks are not configured correctly"
            result.found += "; kmod symlink validation failed"
        return result
