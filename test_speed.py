import asyncio
from unittest.mock import Mock

class DummyWriter:
    def write(self, data):
        pass

w = DummyWriter()
import sys
sys.path.append("/app/core")
sys.path.append("/app/src")
import gui_bridge
gui_bridge._wrap_writer_for_down(w)
w.write(b"hello")

import stats
print(stats.snapshot())
