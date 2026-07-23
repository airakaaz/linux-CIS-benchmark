import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path


def save_json(results: list) -> Path:
    reports = Path("reports")
    reports.mkdir(exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.json")
    path = reports / filename

    with path.open("w", encoding="utf-8") as f:
        json.dump(
            [asdict(r) for r in results],
            f,
            indent=4,
            ensure_ascii=False,
        )

    return path


def save_text(results: list) -> Path:
    reports = Path("reports")
    reports.mkdir(exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.json")
    path = reports / filename

    with path.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(f"rule id: {r.rule_id}")
            f.write(f"title: {r.title}")
            f.write(f"message: {r.message}")
            f.write(f"expected: {r.expected}")
            f.write(f"found: {r.found}")
            f.write("\n")

    return path


FORMATS = {
    "text": save_text,
    "json": save_json,
}
