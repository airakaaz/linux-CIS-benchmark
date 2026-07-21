from typing import Type
from core.module import Module
from core.result import ScanResult
from core.rule import CISRule, Mode


class ScanEngine:
    def __init__(self):
        self._modules: list[Module] = []

    def register(self, *modules: Module):
        self._modules.extend(modules)

    def run(self) -> list[ScanResult]:
        results: list[ScanResult] = []
        manual_checks = []

        for mod in self._modules:
            for rule in mod.rules:
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
