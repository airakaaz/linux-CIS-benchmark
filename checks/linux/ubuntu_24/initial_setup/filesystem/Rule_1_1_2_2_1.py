from ._Base_1_1_2 import SeparatePartitionRule


class Rule_1_1_2_2_1(SeparatePartitionRule):
    _MOUNT_POINT = "/dev/shm"

    rule_id = "1.1.2.2.1"
    title = f"Ensure {_MOUNT_POINT} is tmpfs or a separate partition"
    server_lvl = 1
    workstation_lvl = 1
