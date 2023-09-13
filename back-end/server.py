import sqlite3
import hashlib
import asyncio
import websockets

async def client_handler(websocket, path):
    while True:
        message = await websocket.recv()

        if message == "auth":
            username = await websocket.recv()
            password = await websocket.recv()

            cx = sqlite3.connect("Users.db")
            cu = cx.cursor()

            password = hashlib.sha256(password.encode()).hexdigest()

            cu.execute("SELECT * FROM UserData WHERE Username = ? AND Password = ?", (username, password))
            if cu.fetchall():
                print("Authentication complete, have plesent stay!")
                #placeholder for account actions
            else:
                print("Authentication failed, please typ again")
        else:
            print(message)
    

server = websockets.serve(client_handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()