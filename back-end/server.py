import sqlite3
import hashlib
import asyncio
import websockets
import http.server
import socketserver
import threading
import secrets
import json

ADDRESS = "localhost"
PORT = 8000

clients = {}

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = './front-end/index.html'  # Default to serving index.html
        else:
            # Handle other paths as needed
            self.path = './front-end' + self.path

        # Call the parent class method to handle the file request
        return super().do_GET()

def run_http_server():
    Handler = MyHTTPRequestHandler
    with socketserver.TCPServer((ADDRESS, PORT), Handler) as httpd:
        print("HTTP server serving at port", PORT)
        httpd.serve_forever()

async def client_handler(websocket):
    user_id = secrets.token_bytes(12)   # identify user
    clients[user_id] = websocket    #stores connections for seperate clients

    try:
        while websocket.open:
            message = await clients[user_id].recv()
            message = json.loads(message)

            if message["type"] == "auth": #checks it its a authentication request or status message
                username = message["username"]
                password = message["password"]

                #connects to database containing users
                cx = sqlite3.connect("Users.db")
                cu = cx.cursor()

                password = hashlib.sha256(password.encode()).hexdigest() #converts password to hash for comparasin against database

                #checks database for matching users
                cu.execute("SELECT * FROM UserData WHERE Username = ? AND Password = ?", (username, password)) #note the use of whitelist to stop sql injections
                if cu.fetchall():
                    print(f"Authentication complete for: {username}")
                    await clients[user_id].send("completed")
                    #placeholder for account actions
                else:
                    print("Authentication failed, please typ again")
                    await clients[user_id].send("failed")
            else:
                await clients[user_id].send("connection!")
    finally:
        del clients[user_id]
    

http_thread = threading.Thread(target=run_http_server)

http_thread.start() #starts the http server

#starts the websocket server
server = websockets.serve(client_handler, ADDRESS, 8001)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()

