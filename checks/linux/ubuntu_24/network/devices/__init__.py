from core.module import Module

from .Rule_3_1_2 import Rule_3_1_2
from .Rule_3_1_3 import Rule_3_1_3

rules = [
    Rule_3_1_2,
    Rule_3_1_3,
]

devices = Module(name="devices", rules=rules)
