from dataclasses import dataclass
import re

from utils.command import run


@dataclass(slots=True)
class packageResult:
    valid: bool
    anomalies: set[str]


def installed(*packages: str) -> packageResult:
    missing = set()
    for package in packages:
        if not run(f"dpkg-query -W {package}").ok:
            missing.add(package)

    return packageResult(valid=not missing, anomalies=missing)


def up_to_date(*packages: str) -> packageResult:
    outdated = set()
    for package in packages:
        result = run("apt list --upgradable")
        if re.search(rf"^{package}\b", result.stdout):
            outdated.add(package)

    return packageResult(valid=not outdated, anomalies=outdated)


def not_installed(*packages: str) -> packageResult:
    installed = set()
    for package in packages:
        if run(f"dpkg-query -W {package}").ok:
            installed.add(package)

    return packageResult(valid=not installed, anomalies=installed)
