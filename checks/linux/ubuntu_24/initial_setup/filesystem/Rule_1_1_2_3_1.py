from ._Base_1_1_2 import SeparatePartitionRule


class Rule_1_1_2_3_1(SeparatePartitionRule):
    _MOUNT_POINT = "/home"

    rule_id = "1.1.2.3.1"
    title = f"Ensure separate partition exists for {_MOUNT_POINT}"
