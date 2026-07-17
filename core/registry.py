from typing import Type

from core.rule import CISRule


class RuleRegistry:
    def __init__(self):
        self._rules: dict[str, Type[CISRule]] = {}

    def register(self, rule: Type[CISRule]) -> None:
        self._rules[rule.rule_id] = rule

    def register_many(self, *rules: Type[CISRule]) -> None:
        for rule in rules:
            self._rules[rule.rule_id] = rule

    @property
    def rules_dict(self) -> dict[str, Type[CISRule]]:
        return self._rules.copy()

    @property
    def rules_list(self) -> list[Type[CISRule]]:
        return list(self._rules.values())
