from utils.command import run


def get_enabled_state(service: str) -> str:
    result = run(f"systemctl is-enabled {service}")
    return result.stdout.strip()


def is_enabled(service: str) -> bool:
    return get_enabled_state(service).startswith("enabled")


def is_active(service: str) -> bool:
    result = run(f"systemctl is-active {service}")
    return result.stdout.strip() == "active"
