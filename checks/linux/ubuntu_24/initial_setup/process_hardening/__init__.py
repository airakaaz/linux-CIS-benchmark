from core.module import Module

from .Rule_1_5_1 import Rule_1_5_1
from .Rule_1_5_2 import Rule_1_5_2
from .Rule_1_5_3 import Rule_1_5_3
from .Rule_1_5_4 import Rule_1_5_4
from .Rule_1_5_5 import Rule_1_5_5
from .Rule_1_5_6 import Rule_1_5_6
from .Rule_1_5_7 import Rule_1_5_7
from .Rule_1_5_8 import Rule_1_5_8
from .Rule_1_5_9 import Rule_1_5_9
from .Rule_1_5_11 import Rule_1_5_11
from .Rule_1_5_12 import Rule_1_5_12

rules = [
    Rule_1_5_1,
    Rule_1_5_2,
    Rule_1_5_3,
    Rule_1_5_4,
    Rule_1_5_5,
    Rule_1_5_6,
    Rule_1_5_7,
    Rule_1_5_8,
    Rule_1_5_9,
    Rule_1_5_11,
    Rule_1_5_12,
]

process_hardening = Module(name="process_hardening", rules=rules)
