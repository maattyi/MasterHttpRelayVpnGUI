import sys
sys.path.append("/app/core")
sys.path.append("/app/src")

class MockWriter:
    def write(self, data):
        pass

w = MockWriter()
import gui_bridge
gui_bridge._wrap_writer_for_down(w)
w.write(b"hello")

w.writelines([b"hello", b"world"])
import stats
print(stats.snapshot())
