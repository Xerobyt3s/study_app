from datetime import date
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
            try:    #trys to recive message from client
                message = await clients[user_id].recv()
            except:
                break
            message = json.loads(message)

            if message["type"] == "auth": #checks it its a authentication request or status message
                username = message["username"]
                password = message["password"]

                #connects to database containing users
                cx = sqlite3.connect("Data.db")
                cu = cx.cursor()

                password = hashlib.sha256(password.encode()).hexdigest() #converts password to hash for comparasin against database

                #checks database for matching users
                cu.execute("SELECT Permission FROM UserData WHERE Username = ? AND Password = ?", (username, password))
                auth = cu.fetchone() #note the use of whitelist to stop sql injections
                if auth:
                    print(f"Authentication complete for: {username}")
                    event = {"type": "auth", "auth_status": True, "permission": auth}
                    await clients[user_id].send(json.dumps(event))
                else:
                    print("Authentication failed, please typ again")
                    event = {"type": "auth", "auth_status": False}
                    await clients[user_id].send(json.dumps(event))
            
            elif message["type"] == "request": #expects a item and from variable
                #retrive data from request
                username = message["username"]
                password = message["password"]
                table = message["from"]
                item = message["item"]

                #connects to database containing users
                cx = sqlite3.connect("Data.db")
                cu = cx.cursor()

                password = hashlib.sha256(password.encode()).hexdigest() #converts password to hash for comparasin against database

                #checks database for matching users
                cu.execute("SELECT * FROM UserData WHERE Username = ? AND Password = ?", (username, password)) #note the use of whitelist to stop sql injections
                if cu.fetchall():
                    try:
                        #tries to connect to database relevant to request
                        cx = sqlite3.connect(f"Data.db")
                        cu = cx.cursor()
                    except:
                        #if it fails to connect to database, sends request back assuming the database does not exist
                        event = {"type": "answer", "content": None, "reason": "404: database not found"}
                        await clients[user_id].send(json.dumps(event))
                        break
                    
                    #tries to retrive the item relevant to the request from the database
                    cu.execute(f"SELECT {item} FROM {table} WHERE Username = ? AND Password = ?", (username, password))
                    result = cu.fetchone()

                    if result:
                        #sends the result back to client
                        event = {"type": "answer", "content": result, "reason": "item fetched"}
                        await clients[user_id].send(json.dumps(event))
                    else:
                        #informs client that the item requested does not exist
                        event = {"type": "answer", "content": None, "reason": "404: item not found"}
                        await clients[user_id].send(json.dumps(event))
                else:
                    #informs client that the authentication failed
                    event = {"type": "answer", "content": None, "reason": "auth failed"}
                    await clients[user_id].send(json.dumps(event))

            elif message["type"] == "pull": #this is a placeholder and expects a sql command
                #retrive data from request 
                quarry = message["quarry"]

                cx = sqlite3.connect("Data.db")
                cu = cx.cursor()

                #tries to execute the quarry 
                try:
                    cu.execute(quarry)
                    result = cu.fetchall()
                    event = {"type": "answer", "content": result, "reason": "quarry executed"}
                    await clients[user_id].send(json.dumps(event))
                except:
                    #if it fails to execute the quarry, informs the client
                    event = {"type": "answer", "content": None, "reason": "quarry failed"}
                    await clients[user_id].send(json.dumps(event))
                    break
            
            elif message["type"] == "create_user": #expects a username, password and permission variable
                username = message["username"]
                password = message["password"]
                permission = message["permission"]

                #connects to database containing users
                cx = sqlite3.connect("Data.db")
                cu = cx.cursor()

                password = hashlib.sha256(password.encode()).hexdigest()

                #checks database for matching users
                cu.execute("SELECT * FROM UserData WHERE Username = ?", (username,)) #note the use of whitelist to stop sql injections
                if not cu.fetchall():
                    #if the user does not exist, creates the user
                    cu.execute("INSERT INTO UserData (Username, Password, Permission) VALUES (?, ?, ?)", (username, password, permission))
                    cx.commit()
                    event = {"type": "answer", "content": None, "reason": "user created"}
                    await clients[user_id].send(json.dumps(event))
                    print(f"User created: {username}")
                else:
                    event = {"type": "answer", "content": None, "reason": "user already exists"}
                    await clients[user_id].send(json.dumps(event))

            elif message["type"] == "create_definition":
                username = message["username"]
                word = message["word"]
                definition = message["definition"]
                subject = message["subject"]
                edit_date = date.today().strftime("%d/%m/%Y")

                #connects to database containing users
                cx = sqlite3.connect("Data.db")
                cu = cx.cursor()

                #checks database for matching words
                cu.execute("SELECT * FROM Definitions WHERE Word = ?", (word,))

                if not cu.fetchall():
                    #if the word does not exist, creates the word
                    cu.execute("INSERT INTO Definitions (Word, Definition, Subject, Author, EditDate) VALUES (?, ?, ?, ?, ?)", (word, definition, subject, username, edit_date))
                    cx.commit()
                    event = {"type": "answer", "content": None, "reason": "definition created"}
                    await clients[user_id].send(json.dumps(event))
                    print(f"Definition created: {word}")
                else:
                    cu.execute("UPDATE Definitions SET Definition = ?, Subject = ?, Author = ?, EditDate = ? WHERE Word = ?", (definition, subject, username, edit_date, word))
                    cx.commit()
                    event = {"type": "answer", "content": None, "reason": "definition edited"}
                    await clients[user_id].send(json.dumps(event))
                    print(f"Definition edited: {word}")

                cu.execute("SELECT * FROM Definitions WHERE Word = ?", (word,))
                new_word = cu.fetchone()
                event = {"type": "updated_definiton", "content": new_word, "reason": "definiton was updated"}
                for client in clients:
                    await client.send(json.dumps(event))
            
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

