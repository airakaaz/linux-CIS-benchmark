from core.registry import RuleRegistry
from core.result import ScanResult
from core.rule import Mode


class ScanEngine:
    def __init__(self, registry: RuleRegistry):
        self.registry = registry

    def run(self) -> list[ScanResult]:
        results: list[ScanResult] = []
        manual_checks = []

        for rule in self.registry.rules:
            if rule.mode == Mode.AUTOMATIC:
                results.append(rule().check())
            else:
                manual_checks.append(rule)

        return results
