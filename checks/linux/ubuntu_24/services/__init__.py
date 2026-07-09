from .job_scheduler import *
from .client import *

rules = []
rules.extend(job_scheduler.rules)
rules.extend(client.rules)
