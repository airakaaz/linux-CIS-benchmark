from ._Base_1_2_1 import DirectoryAccess


class Rule_1_2_1_7(DirectoryAccess):
    rule_id = "1.2.1.7"

    _PATH = "/usr/share/keyrings"
    _MAX_ACCESS = 0o775

    title = f"Ensure access to {_PATH} directory is configured"
