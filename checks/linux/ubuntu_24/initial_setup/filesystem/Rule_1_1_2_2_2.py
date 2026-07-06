from ._Base_1_1_2 import MountOptionRule


class Rule_1_1_2_2_2(MountOptionRule):
    rule_id = "1.1.2.2.2"
    _MOUNT_POINT = "/dev/shm"
    _OPTION = "nodev"
    title = f"Ensure {_OPTION} option set on {_MOUNT_POINT} partition"
