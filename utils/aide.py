from pathlib import Path
import re
import shlex
import shutil

from utils.command import CommandResult, run


AIDE_AUDIT_TOOLS = (
    "auditctl",
    "auditd",
    "ausearch",
    "aureport",
    "autrace",
    "augenrules",
)
AIDE_REQUIRED_OPTIONS = ("p", "i", "n", "u", "g", "s", "b", "acl", "xattrs", "sha512")


def executable() -> str | None:
    return shutil.which("aide")


def configuration_file() -> Path | None:
    preferred = Path("/etc/aide/aide.conf")
    if preferred.is_file():
        return preferred
    try:
        files = sorted(path for path in Path("/etc").rglob("aide.conf") if path.is_file())
    except OSError:
        return None
    return files[0] if files else None


def profile(path: Path) -> CommandResult:
    command = executable()
    config = configuration_file()
    if command is None or config is None:
        return CommandResult(stdout="", stderr="aide or aide.conf not found", returncode=1)
    return run(
        f"{shlex.quote(command)} --config {shlex.quote(str(config))} "
        f"-p f:{shlex.quote(str(path))}"
    )


def has_options(output: str, options: tuple[str, ...] = AIDE_REQUIRED_OPTIONS) -> bool:
    return all(
        re.search(rf"(?:^|[\s+]){re.escape(option)}(?=$|[\s+])", output)
        for option in options
    )
