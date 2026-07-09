from dataclasses import dataclass
import re

from utils.command import run


@dataclass(slots=True)
class packageResult:
    valid: bool
    anomalies: set[str | tuple[str]]


def installed(*packages: str | tuple[str]) -> packageResult:
    missing = set()
    for package in packages:
        if type(package) is str:
            package = tuple(
                package,
            )
        found = False
        for alt in package:
            if run(f"dpkg-query -W {alt}").ok:
                found = True
        if not found:
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
