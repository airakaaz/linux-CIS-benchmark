from core.module import Module

from .Rule_1_2_1_2 import Rule_1_2_1_2
from .Rule_1_2_1_3 import Rule_1_2_1_3
from .Rule_1_2_1_4 import Rule_1_2_1_4
from .Rule_1_2_1_5 import Rule_1_2_1_5
from .Rule_1_2_1_6 import Rule_1_2_1_6
from .Rule_1_2_1_7 import Rule_1_2_1_7
from .Rule_1_2_1_8 import Rule_1_2_1_8
from .Rule_1_2_1_9 import Rule_1_2_1_9
from .Rule_1_2_1_1 import Rule_1_2_1_1
from .Rule_1_2_2_1 import Rule_1_2_2_1

rules = [
    Rule_1_2_1_2,
    Rule_1_2_1_3,
    Rule_1_2_1_4,
    Rule_1_2_1_5,
    Rule_1_2_1_6,
    Rule_1_2_1_7,
    Rule_1_2_1_8,
    Rule_1_2_1_9,
    Rule_1_2_1_1,
    Rule_1_2_2_1,
]

package_management = Module(name="package_management", rules=rules)
