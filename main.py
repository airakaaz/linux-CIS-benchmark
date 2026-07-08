import checks.linux.ubuntu_24 as ubuntu_24
from core import ScanEngine, RuleRegistry


registry = RuleRegistry()
registry.register_many(*ubuntu_24.rules)

engine = ScanEngine(registry)
results = engine.run()


total = len(results)
passed = 0

for result in results:
    if result.passed:
        passed += 1

    print("id       :", result.rule_id)
    print("title    :", result.title)
    print("expected :", result.expected)
    print("found    :", result.found)
    print("passed   :", result.passed)
    print("message  :", result.message)
    print()

print("=============")
print(f"score    : {passed}/{total}")
