from core.module import Module

from .Rule_2_4_1_1 import Rule_2_4_1_1
from .Rule_2_4_1_2 import Rule_2_4_1_2
from .Rule_2_4_1_3 import Rule_2_4_1_3
from .Rule_2_4_1_4 import Rule_2_4_1_4
from .Rule_2_4_1_5 import Rule_2_4_1_5
from .Rule_2_4_1_6 import Rule_2_4_1_6
from .Rule_2_4_1_7 import Rule_2_4_1_7
from .Rule_2_4_1_8 import Rule_2_4_1_8
from .Rule_2_4_1_9 import Rule_2_4_1_9
from .Rule_2_4_2_1 import Rule_2_4_2_1

rules = [
    Rule_2_4_1_1,
    Rule_2_4_1_2,
    Rule_2_4_1_3,
    Rule_2_4_1_4,
    Rule_2_4_1_5,
    Rule_2_4_1_6,
    Rule_2_4_1_7,
    Rule_2_4_1_8,
    Rule_2_4_1_9,
    Rule_2_4_2_1,
]

job_scheduler = Module(name="job_scheduler", rules=rules)
