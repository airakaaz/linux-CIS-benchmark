from utils.command import run


def is_installed(package: str) -> bool:
    return run(f"dpkg-query -W {package}").ok
