import sqlite3
import hashlib
import asyncio
import websockets

async def client_handler(websocket, path):
    while True:
        data = await websocket.recv()
        print(f"Data Recieved: {data}")
    

server = websockets.serve(client_handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()