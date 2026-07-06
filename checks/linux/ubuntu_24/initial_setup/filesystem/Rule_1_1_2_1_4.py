from ._Base_1_1_2 import MountOptionRule


class Rule_1_1_2_1_4(MountOptionRule):
    rule_id = "1.1.2.1.4"
    _MOUNT_POINT = "/tmp"
    _OPTION = "noexec"
    title = f"Ensure {_OPTION} option set on {_MOUNT_POINT} partition"
