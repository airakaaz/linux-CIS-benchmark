from core.module import Module

from .Rule_5_4_1_1 import Rule_5_4_1_1
from .Rule_5_4_1_3 import Rule_5_4_1_3
from .Rule_5_4_1_4 import Rule_5_4_1_4
from .Rule_5_4_1_5 import Rule_5_4_1_5
from .Rule_5_4_1_6 import Rule_5_4_1_6
from .Rule_5_4_2_1 import Rule_5_4_2_1
from .Rule_5_4_2_2 import Rule_5_4_2_2
from .Rule_5_4_2_3 import Rule_5_4_2_3
from .Rule_5_4_2_4 import Rule_5_4_2_4
from .Rule_5_4_2_5 import Rule_5_4_2_5
from .Rule_5_4_2_6 import Rule_5_4_2_6
from .Rule_5_4_2_7 import Rule_5_4_2_7
from .Rule_5_4_2_8 import Rule_5_4_2_8
from .Rule_5_4_3_1 import Rule_5_4_3_1
from .Rule_5_4_3_2 import Rule_5_4_3_2
from .Rule_5_4_3_3 import Rule_5_4_3_3
from .Rule_5_4_1_2 import Rule_5_4_1_2

rules = [
    Rule_5_4_1_1,
    Rule_5_4_1_3,
    Rule_5_4_1_4,
    Rule_5_4_1_5,
    Rule_5_4_1_6,
    Rule_5_4_2_1,
    Rule_5_4_2_2,
    Rule_5_4_2_3,
    Rule_5_4_2_4,
    Rule_5_4_2_5,
    Rule_5_4_2_6,
    Rule_5_4_2_7,
    Rule_5_4_2_8,
    Rule_5_4_3_1,
    Rule_5_4_3_2,
    Rule_5_4_3_3,
    Rule_5_4_1_2,
]

users = Module(name="users", rules=rules)
