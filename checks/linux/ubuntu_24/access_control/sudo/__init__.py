from core.module import Module

from .Rule_5_2_1 import Rule_5_2_1
from .Rule_5_2_2 import Rule_5_2_2
from .Rule_5_2_3 import Rule_5_2_3
from .Rule_5_2_4 import Rule_5_2_4
from .Rule_5_2_5 import Rule_5_2_5
from .Rule_5_2_6 import Rule_5_2_6
from .Rule_5_2_7 import Rule_5_2_7

rules = [
    Rule_5_2_1,
    Rule_5_2_2,
    Rule_5_2_3,
    Rule_5_2_4,
    Rule_5_2_5,
    Rule_5_2_6,
    Rule_5_2_7,
]

sudo = Module(name="sudo", rules=rules)
