
# Agent B: Asynchronous TCP Server

import asyncio
import json
from tools import *


HOST = "127.0.0.1"
PORT = 9000


async def main():

    server = await asyncio.start_server(
        handle_client,
        HOST,
        PORT
    )

    print(f"Async Agent B listening on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()


asyncio.run(main())
