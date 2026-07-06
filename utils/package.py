from utils.command import run


def is_installed(package: str) -> bool:
    return run(f"dpkg-query -W {package}").ok


def missing(*packages: str) -> list[str]:
    missing: list[str] = []
    for package in packages:
        if not run(f"dpkg-query -W {package}").ok:
            missing.append(package)

    return missing
