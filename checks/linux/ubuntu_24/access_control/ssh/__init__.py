from core.module import Module

from .Rule_5_1_1 import Rule_5_1_1
from .Rule_5_1_2 import Rule_5_1_2
from .Rule_5_1_3 import Rule_5_1_3
from .Rule_5_1_4 import Rule_5_1_4
from .Rule_5_1_5 import Rule_5_1_5
from .Rule_5_1_6 import Rule_5_1_6
from .Rule_5_1_7 import Rule_5_1_7
from .Rule_5_1_8 import Rule_5_1_8
from .Rule_5_1_9 import Rule_5_1_9
from .Rule_5_1_10 import Rule_5_1_10
from .Rule_5_1_11 import Rule_5_1_11
from .Rule_5_1_12 import Rule_5_1_12
from .Rule_5_1_13 import Rule_5_1_13
from .Rule_5_1_14 import Rule_5_1_14
from .Rule_5_1_15 import Rule_5_1_15
from .Rule_5_1_16 import Rule_5_1_16
from .Rule_5_1_17 import Rule_5_1_17
from .Rule_5_1_18 import Rule_5_1_18
from .Rule_5_1_19 import Rule_5_1_19
from .Rule_5_1_20 import Rule_5_1_20
from .Rule_5_1_21 import Rule_5_1_21
from .Rule_5_1_22 import Rule_5_1_22
from .Rule_5_1_23 import Rule_5_1_23
from .Rule_5_1_24 import Rule_5_1_24

rules = [
    Rule_5_1_1,
    Rule_5_1_2,
    Rule_5_1_3,
    Rule_5_1_4,
    Rule_5_1_5,
    Rule_5_1_6,
    Rule_5_1_7,
    Rule_5_1_8,
    Rule_5_1_9,
    Rule_5_1_10,
    Rule_5_1_11,
    Rule_5_1_12,
    Rule_5_1_13,
    Rule_5_1_14,
    Rule_5_1_15,
    Rule_5_1_16,
    Rule_5_1_17,
    Rule_5_1_18,
    Rule_5_1_19,
    Rule_5_1_20,
    Rule_5_1_21,
    Rule_5_1_22,
    Rule_5_1_23,
    Rule_5_1_24,
]

ssh = Module(name="ssh", rules=rules)
