from core.module import Module

from .Rule_6_1_1_1_1 import Rule_6_1_1_1_1
from .Rule_6_1_1_1_2 import Rule_6_1_1_1_2
from .Rule_6_1_1_1_3 import Rule_6_1_1_1_3
from .Rule_6_1_1_1_6 import Rule_6_1_1_1_6
from .Rule_6_1_1_1_7 import Rule_6_1_1_1_7
from .Rule_6_1_1_1_4 import Rule_6_1_1_1_4
from .Rule_6_1_1_1_5 import Rule_6_1_1_1_5

rules = [
    Rule_6_1_1_1_1,
    Rule_6_1_1_1_2,
    Rule_6_1_1_1_3,
    Rule_6_1_1_1_6,
    Rule_6_1_1_1_7,
    Rule_6_1_1_1_4,
    Rule_6_1_1_1_5,
]

journald = Module(name="journald", rules=rules)
