from core.module import Module

from .Rule_1_3_1_1 import Rule_1_3_1_1
from .Rule_1_3_1_2 import Rule_1_3_1_2
from .Rule_1_3_1_3 import Rule_1_3_1_3
from .Rule_1_3_1_4 import Rule_1_3_1_4

rules = [
    Rule_1_3_1_1,
    Rule_1_3_1_2,
    Rule_1_3_1_3,
    Rule_1_3_1_4,
]

apparmor = Module(name="apparmor", rules=rules)
