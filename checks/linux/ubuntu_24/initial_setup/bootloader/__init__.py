from core.module import Module

from .Rule_1_4_1 import Rule_1_4_1
from .Rule_1_4_2 import Rule_1_4_2

rules = [
    Rule_1_4_1,
    Rule_1_4_2,
]

bootloader = Module(name="bootloader", rules=rules)
