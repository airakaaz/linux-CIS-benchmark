from ._Base_7_1 import DirectoryAccess


class Rule_7_1_3(DirectoryAccess):
    rule_id = "7.1.3"

    _PATH = "/etc/group"
    _MAX_ACCESS = 0o644

    title = f"Ensure access to {_PATH} directory is configured"
