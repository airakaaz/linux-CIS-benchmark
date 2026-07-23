from core.module import Module

from .Rule_7_1_1 import Rule_7_1_1
from .Rule_7_1_2 import Rule_7_1_2
from .Rule_7_1_3 import Rule_7_1_3
from .Rule_7_1_4 import Rule_7_1_4
from .Rule_7_1_5 import Rule_7_1_5
from .Rule_7_1_6 import Rule_7_1_6
from .Rule_7_1_7 import Rule_7_1_7
from .Rule_7_1_8 import Rule_7_1_8
from .Rule_7_1_9 import Rule_7_1_9
from .Rule_7_1_10 import Rule_7_1_10
from .Rule_7_1_11 import Rule_7_1_11
from .Rule_7_1_12 import Rule_7_1_12
from .Rule_7_1_13 import Rule_7_1_13

rules = [
    Rule_7_1_1,
    Rule_7_1_2,
    Rule_7_1_3,
    Rule_7_1_4,
    Rule_7_1_5,
    Rule_7_1_6,
    Rule_7_1_7,
    Rule_7_1_8,
    Rule_7_1_9,
    Rule_7_1_10,
    Rule_7_1_11,
    Rule_7_1_12,
    Rule_7_1_13,
]

filesystem = Module(name="filesystem", rules=rules)
