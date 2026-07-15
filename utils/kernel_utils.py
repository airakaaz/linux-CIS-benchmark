import glob
import re
from pathlib import Path

from utils.command import run


def module_symlinks_point_to_kmod() -> bool:
    target = Path("/bin/kmod")
    try:
        target = target.resolve()
    except OSError:
        return False

    for path in (
        "/usr/sbin/lsmod",
        "/usr/sbin/rmmod",
        "/usr/sbin/insmod",
        "/usr/sbin/modinfo",
        "/usr/sbin/modprobe",
        "/usr/sbin/depmod",
    ):
        candidate = Path(path)
        try:
            if not candidate.is_symlink() or candidate.resolve() != target:
                return False
        except OSError:
            return False
    return True


def is_available(module_name: str, mod_type: str) -> bool:
    module_path_part = module_name.replace("-", "/")
    patterns = [
        f"/usr/lib/modules/*/kernel/{mod_type}/{module_path_part}",
        f"/lib/modules/*/kernel/{mod_type}/{module_path_part}",
    ]
    for pattern in patterns:
        for match in glob.glob(pattern):
            path = Path(match)
            if path.is_dir() and any(path.iterdir()):
                return True
    return False


def is_loaded(module_name: str) -> bool:
    result = run("lsmod")
    if not result.ok:
        return False
    return any(
        line.split()[0] == module_name
        for line in result.stdout.splitlines()
        if line.strip()
    )


def get_config(module_name: str) -> dict:
    result = run("modprobe --showconfig")
    blacklisted = False
    install_disabled = False

    if result.ok:
        blacklist_re = re.compile(rf"^\s*blacklist\s+{re.escape(module_name)}\s*$")
        install_re = re.compile(rf"^\s*install\s+{re.escape(module_name)}\s+(\S+)")
        for line in result.stdout.splitlines():
            if blacklist_re.match(line):
                blacklisted = True
                continue
            match = install_re.match(line)
            if match and match.group(1) in ("/bin/false", "/bin/true"):
                install_disabled = True

    return {"blacklisted": blacklisted, "install_disabled": install_disabled}


def wireless_modules() -> list[str]:
    modules: set[str] = set()
    for wireless in Path("/sys/class/net").glob("*/wireless"):
        module = wireless.parent / "device/driver/module"
        try:
            if module.exists():
                modules.add(module.resolve().name)
        except OSError:
            continue
    return sorted(modules)


def is_load_disabled(module_name: str) -> bool:
    result = run(f"modprobe -n -v {module_name}")
    return result.ok and re.search(
        r"^\s*install\s+/bin/(?:true|false)\b", result.stdout, flags=re.MULTILINE
    ) is not None
