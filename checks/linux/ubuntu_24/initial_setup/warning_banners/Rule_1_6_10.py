from ._Base_1_6 import PathAccessRule, get_sshd_banner


class Rule_1_6_10(PathAccessRule):
    rule_id = "1.6.10"
    title = "Ensure access to sshd warning banner is configured"

    _MAX_ACCESS = 0o644
    _PATH = get_sshd_banner()
