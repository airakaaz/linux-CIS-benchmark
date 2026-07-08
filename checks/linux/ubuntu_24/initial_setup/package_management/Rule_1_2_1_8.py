from ._Base_1_2_1 import DirectoryAccess


class Rule_1_2_1_8(DirectoryAccess):
    rule_id = "1.2.1.8"

    _PATH = "/etc/apt/sources.list.d"
    _MAX_ACCESS = 0o775

    title = f"Ensure access to {_PATH} directory is configured"
