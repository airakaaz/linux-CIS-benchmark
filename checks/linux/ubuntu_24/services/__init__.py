from core.module import Module

from .server import server
from .client import client
from .time_sync import time_sync
from .job_scheduler import job_scheduler

subMods = [
    server,
    client,
    time_sync,
    job_scheduler,
]

services = Module(name="services", subMods=subMods)
