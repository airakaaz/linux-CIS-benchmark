from ._Base_7_1 import DirectoryAccess


class Rule_7_1_9(DirectoryAccess):
    rule_id = "7.1.9"

    _PATH = "/etc/shells"
    _MAX_ACCESS = 0o644

    title = f"Ensure access to {_PATH} directory is configured"
