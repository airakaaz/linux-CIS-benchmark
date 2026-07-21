from checks.linux.ubuntu_24 import ubuntu_24
from core import ScanEngine, RuleRegistry


registry = RuleRegistry()
registry.register_many(*ubuntu_24.rules)

engine = ScanEngine(registry)

i = 0
while i not in {2, 3}:
    try:
        i = int(input("1: all checks\n2: choose checks\n"))
    except Exception:
        pass

results = None
match i:
    case 1:
        results = engine.run_all()
    case 2:
        while True:
            rule_id = input("rule(s) id : ")
            if rule_id:
                results = engine.run_matching(rule_id)
                break
            else:
                break

if results:
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
else:
    print("engine didn't run, exiting")
