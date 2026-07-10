from ._Base_1_6 import PathAccessRule
from utils.command import run


def get_sshd_banner() -> str:
    result = run("sshd -T")

    if not result.ok:
        return ""

    for line in result.stdout.splitlines():
        if line.startswith("banner "):
            banner = line.split(maxsplit=1)[1]
            if banner.lower() == "none":
                return ""
            return banner

    return ""


class Rule_1_6_10(PathAccessRule):
    rule_id = "1.6.10"
    title = "Ensure access to sshd warning banner is configured"

    _MAX_ACCESS = 0o644
    _PATH = get_sshd_banner()
