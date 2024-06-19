import asyncio
import websockets
import os


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


async def main():
    port = int(os.environ.get("WS_PORT", 8081))
    async with websockets.serve(echo, "0.0.0.0", port):
        await asyncio.Future()


asyncio.run(main())
