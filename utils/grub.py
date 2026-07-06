import re
from pathlib import Path

_GRUB_CFG = "/boot/grub/grub.cfg"


def kernel_cmdline_has(param: str, path: str = _GRUB_CFG) -> bool:
    cfg = Path(path)
    if not cfg.is_file():
        return False

    pattern = re.compile(rf"\b{re.escape(param)}\b")
    for line in cfg.read_text(errors="ignore").splitlines():
        if re.match(r"^\s*linux", line) and pattern.search(line):
            return True
    return False
