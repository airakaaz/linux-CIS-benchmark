from checks.templates.path_access import PathAccessRule, MultiPathsAccessRule
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
