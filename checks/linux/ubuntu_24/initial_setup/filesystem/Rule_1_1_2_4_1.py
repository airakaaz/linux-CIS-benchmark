from ._Base_1_1_2 import SeparatePartitionRule


class Rule_1_1_2_4_1(SeparatePartitionRule):
    _MOUNT_POINT = "/var"

    rule_id = "1.1.2.4.1"
    title = f"Ensure separate partition exists for {_MOUNT_POINT}"
