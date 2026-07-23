from core.module import Module

from .Rule_6_1_2_1 import Rule_6_1_2_1
from .Rule_6_1_2_2 import Rule_6_1_2_2
from .Rule_6_1_2_3 import Rule_6_1_2_3
from .Rule_6_1_2_6 import Rule_6_1_2_6
from .Rule_6_1_2_8 import Rule_6_1_2_8
from .Rule_6_1_2_9 import Rule_6_1_2_9
from .Rule_6_1_2_4 import Rule_6_1_2_4
from .Rule_6_1_2_5 import Rule_6_1_2_5
from .Rule_6_1_2_7 import Rule_6_1_2_7
from .Rule_6_1_2_10 import Rule_6_1_2_10

rules = [
    Rule_6_1_2_1,
    Rule_6_1_2_2,
    Rule_6_1_2_3,
    Rule_6_1_2_6,
    Rule_6_1_2_8,
    Rule_6_1_2_9,
    Rule_6_1_2_4,
    Rule_6_1_2_5,
    Rule_6_1_2_7,
    Rule_6_1_2_10,
]

rsyslog = Module(name="rsyslog", rules=rules)
