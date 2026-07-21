from core.rule import CISRule


class Module:
    def __init__(
        self,
        name: str,
        subMods: list[Module] | None = None,
        rules: list[CISRule] | None = None,
    ):
        self.name = name
        self._subModules = subMods if subMods else []
        self._rules = rules if rules else []

    @property
    def rules(self) -> list[CISRule]:
        r = self._rules.copy()
        for mod in self._subModules:
            r.extend(mod.rules)
        return r

    @property
    def subModules(self) -> list[Module]:
        return self._subModules.copy()
