from utils.command import run


def get_enabled_state(unit: str) -> str:
    result = run(f"systemctl is-enabled {unit}")
    return (result.stdout or result.stderr).strip()
