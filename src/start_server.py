import asyncio
import websockets
import logging

from websocket_server import WebsocketServer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ws_server = WebsocketServer()
    asyncio.run(ws_server.start("", 8000))
