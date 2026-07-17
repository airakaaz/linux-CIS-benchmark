import re
from core.registry import RuleRegistry
from core.result import ScanResult
from core.rule import Mode


class ScanEngine:
    def __init__(self, registry: RuleRegistry):
        self.registry = registry

    def _run(self, rules: list) -> list[ScanResult]:
        results: list[ScanResult] = []
        manual_checks = []

        for rule in rules:
            if rule.mode == Mode.AUTOMATIC:
                try:
                    results.append(rule().check())
                except Exception as e:
                    results.append(
                        ScanResult(
                            rule_id=rule.rule_id,
                            title=rule.title,
                            passed=False,
                            message=f"check failed due to Exception: {e}",
                        )
                    )
            else:
                manual_checks.append(rule)

        return results

    def run_all(self):
        return self._run(self.registry.rules_list)

    def run_matching(self, rule_id: str):
        valid_id = re.compile(re.escape(rule_id))
        rules = [
            rule
            for rule_id, rule in self.registry.rules_dict.items()
            if valid_id.match(rule_id)
        ]

        return self._run(rules)
