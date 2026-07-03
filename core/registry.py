from typing import Type

from core.rule import CISRule


class RuleRegistry:
    def __init__(self):
        self._rules: list[Type[CISRule]] = []

    def register(self, rule: Type[CISRule]) -> None:
        self._rules.append(rule)

    def register_many(self, *rules: Type[CISRule]) -> None:
        self._rules.extend(rules)

    @property
    def rules(self) -> list[Type[CISRule]]:
        return self._rules.copy()

