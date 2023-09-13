import sqlite3
import hashlib
from socket import *
import threading

#creates a socket for wireless data transfer, note that all date will need to be encoded to be sent
server = socket(AF_INET, SOCK_STREAM)
server.bind(("10.31.13.77", 9993)) #Change to localhost if you dont want to use my server for authentication

server.listen()

def ClientHandeling(c):
    while True:
        message = c.recv(1024)
        print(message)
        

while True:
    client, addr = server.accept()
    threading.Thread(target=ClientHandeling, args=(client,)).start()
    