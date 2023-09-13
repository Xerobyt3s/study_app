import sqlite3
import hashlib
import asyncio
import websockets
import http.server
import socketserver
import threading

PORT = 8000

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
    with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
        print("HTTP server serving at port", PORT)
        httpd.serve_forever()

async def client_handler(websocket, path):
    print("server started")
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
                print(f"Authentication complete for: {username}")
                await websocket.send("completed")
                #placeholder for account actions
            else:
                print("Authentication failed, please typ again")
                await websocket.send("failed")
        else:
            print(message)


server = websockets.serve(client_handler, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()

http_thread = threading.Thread(target=run_http_server)

http_thread.start()