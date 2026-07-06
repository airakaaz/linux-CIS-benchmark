from ._Base_1_1_2 import MountOptionRule


class Rule_1_1_2_6_3(MountOptionRule):
    rule_id = "1.1.2.6.3"
    _MOUNT_POINT = "/var/log"
    _OPTION = "nosuid"
    title = f"Ensure {_OPTION} option set on {_MOUNT_POINT} partition"
