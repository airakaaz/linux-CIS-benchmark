from utils.command import run


def get_mount_options(mount_point: str) -> set[str] | None:
    result = run(f"findmnt -kn {mount_point}")
    if not result.ok or not result.stdout.strip():
        return None

    # findmnt -kn output: TARGET SOURCE FSTYPE OPTIONS
    parts = result.stdout.split()
    if len(parts) < 4:
        return None

    return set(parts[-1].split(","))
