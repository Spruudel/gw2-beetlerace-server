import asyncio
import json
import logging

import websockets


class WebsocketServer:
    rooms = dict()

    async def speedometer_handler(self, ws, room):
        logging.info(f"Speedometer joined [{room}]")
        if room not in self.rooms:
            self.rooms[room] = {
                "maps": set(),
                "speedometer": set()
            }
        self.rooms[room]["speedometer"].add(ws)

        try:
            async for msg in ws:
                if room in self.rooms:
                    websockets.broadcast(self.rooms[room]["maps"], msg)
        except websockets.ConnectionClosedError:
            pass

        # connection closed
        if len(self.rooms[room]["speedometer"]) > 1 or self.rooms[room]["maps"]:
            self.rooms[room]["speedometer"].remove(ws)
        else:
            del self.rooms[room]

    async def map_handler(self, ws, room):
        logging.info(f"Map joined [{room}]")

        # create room if necessary
        if room not in self.rooms:
            self.rooms[room] = {
                "maps": set(),
                "speedometer": set()
            }
        self.rooms[room]["maps"].add(ws)

        try:
            async for msg in ws:
                websockets.broadcast(self.rooms[room]["speedometer"], msg)
        except websockets.ConnectionClosedError:
            pass

        # connection closed
        if len(self.rooms[room]["maps"]) > 1 or self.rooms[room]["speedometer"]:
            self.rooms[room]["maps"].remove(ws)
        else:
            del self.rooms[room]

    async def handler(self, ws):
        logging.info(f"Connection opened: {ws.id}")

        try:
            msg = await ws.recv()
        except websockets.ConnectionClosedError:
            return

        event = json.loads(msg)

        assert event["type"] == "init"
        client = event["client"]
        room = str(event["room"])

        if client == "speedometer":
            await self.speedometer_handler(ws, room)
        elif client == "map":
            await self.map_handler(ws, room)
        else:
            return

        logging.info(f"Connection closed: {ws.id}")

    async def start(self, hostname, port):
        async with websockets.serve(self.handler, hostname, port):
            await asyncio.Future()
