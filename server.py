import asyncio

class Server:
    def __init__(self, port: int):
        self._port = port

    async def run_server(self):
        while True:
            await asyncio.sleep(60)
