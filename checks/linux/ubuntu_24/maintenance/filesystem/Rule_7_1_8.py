from ._Base_7_1 import DirectoryAccess


class Rule_7_1_8(DirectoryAccess):
    rule_id = "7.1.8"

    _PATH = "/etc/gshadow-"
    _MAX_ACCESS = 0o640

    title = f"Ensure access to {_PATH} directory is configured"
