from dataclasses import dataclass
import re

from utils.command import run


@dataclass(slots=True)
class packageResult:
    valid: bool
    anomalies: set[str]


def installed(*packages: str | tuple[str, ...]) -> packageResult:
    missing: set[str] = set()
    for package in packages:
        if type(package) is str:
            package = (package,)
        found = False
        for alt in package:
            if run(f"dpkg-query -s {alt}").ok:
                found = True
        if not found:
            missing.add(" or ".join(package))

    return packageResult(valid=not missing, anomalies=missing)


def up_to_date(*packages: str) -> packageResult:
    outdated = set()
    for package in packages:
        result = run("apt list --upgradable")
        if re.search(rf"^{package}\b", result.stdout):
            outdated.add(package)

    return packageResult(valid=not outdated, anomalies=outdated)


def not_installed(*packages: str, mode: str = "s") -> packageResult:
    installed = set()
    match mode:
        case "s":
            for package in packages:
                if run(f"dpkg-query -s {package}").ok:
                    installed.add(package)
        case "l":
            dpkg_list = run("dpkg-query -l").stdout
            for package in packages:
                pattern = re.compile(f"{package}")
                if pattern.search(dpkg_list):
                    installed.add(package)

    return packageResult(valid=not installed, anomalies=installed)


def dependents(package: str) -> set[str]:
    result = run(f"apt-cache rdepends --installed {package}")
    if not result.ok:
        return set()

    lines = result.stdout.splitlines()
    try:
        start = next(
            i for i, line in enumerate(lines) if line.strip() == "Reverse Depends:"
        )
    except StopIteration:
        return set()

    found: set[str] = set()
    for line in lines[start + 1 :]:
        name = line.strip().lstrip("|").strip()
        if name and name != package:
            found.add(name)
    return found


def is_dependency(package: str) -> bool:
    return bool(dependents(package))
