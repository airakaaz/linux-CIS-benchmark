from utils.command import run


def is_enabled(service: str) -> bool:
    result = run(f"systemctl is-enabled {service}")
    return result.stdout.strip().startswith("enabled")


def is_active(service: str) -> bool:
    result = run(f"systemctl is-active {service}")
    return result.stdout.strip() == "active"
