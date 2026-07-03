from core.registry import RuleRegistry
from core.result import ScanResult


class ScanEngine:
    def __init__(self, registry: RuleRegistry):
        self.registry = registry

    def run(self) -> list[ScanResult]:
        results: list[ScanResult] = []

        for rule_cls in self.registry.rules:
            rule = rule_cls()
            results.append(rule.check())

        return results
