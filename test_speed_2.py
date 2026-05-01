import sys
sys.path.append("/app/core")
sys.path.append("/app/src")
import gui_bridge
import asyncio

class DummyReader:
    async def read(self, n=-1):
        return b"hello"
    async def readline(self):
        return b"hello"
    async def readexactly(self, n):
        return b"hello"

r = DummyReader()
gui_bridge._wrap_reader_for_up(r)
async def main():
    await r.read(5)
    import stats
    print(stats.snapshot())

asyncio.run(main())
