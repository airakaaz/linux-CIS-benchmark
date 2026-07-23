from core.module import Module

from .Rule_3_1_2 import Rule_3_1_2
from .Rule_3_1_3 import Rule_3_1_3
from .Rule_3_1_1 import Rule_3_1_1

rules = [
    Rule_3_1_2,
    Rule_3_1_3,
    Rule_3_1_1,
]

devices = Module(name="devices", rules=rules)
