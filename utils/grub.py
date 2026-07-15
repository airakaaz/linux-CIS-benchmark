import re
from pathlib import Path

_GRUB_CFG = "/boot/grub/grub.cfg"


def linux_cmdlines() -> list[str]:
    lines: list[str] = []
    for path in Path("/boot").rglob("grub.cfg"):
        if not path.is_file():
            continue
        try:
            lines.extend(
                line for line in path.read_text(errors="ignore").splitlines()
                if re.match(r"^\s*linux", line)
            )
        except OSError:
            continue
    return lines


def kernel_cmdline_has(param: str, path: str = _GRUB_CFG) -> bool:
    cfg = Path(path)
    if not cfg.is_file():
        return False

    pattern = re.compile(rf"\b{re.escape(param)}\b")
    for line in cfg.read_text(errors="ignore").splitlines():
        if re.match(r"^\s*linux", line) and pattern.search(line):
            return True
    return False
