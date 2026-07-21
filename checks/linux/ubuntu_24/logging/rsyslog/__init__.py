from core.module import Module

from .Rule_6_1_2_1 import Rule_6_1_2_1
from .Rule_6_1_2_2 import Rule_6_1_2_2
from .Rule_6_1_2_3 import Rule_6_1_2_3
from .Rule_6_1_2_6 import Rule_6_1_2_6
from .Rule_6_1_2_8 import Rule_6_1_2_8
from .Rule_6_1_2_9 import Rule_6_1_2_9

rules = [
    Rule_6_1_2_1,
    Rule_6_1_2_2,
    Rule_6_1_2_3,
    Rule_6_1_2_6,
    Rule_6_1_2_8,
    Rule_6_1_2_9,
]

rsyslog = Module(name="rsyslog", rules=rules)
