from dataclasses import dataclass


@dataclass(slots=True)
class ScanResult:
    rule_id: str
    title: str
    passed: bool
    message: str
    expected: str | None = None
    found: str | None = None
