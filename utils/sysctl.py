from utils.command import run


def get(name: str) -> str | None:
    result = run(f"sysctl -n {name}")

    if not result.ok:
        return None

    return result.stdout
