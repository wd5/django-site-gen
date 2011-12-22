import time

from huey.decorators import queue_command
from app import invoker


@queue_command(invoker)
def test_command(n):
    time.sleep(n)
    return n
