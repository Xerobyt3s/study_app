import sqlite3
import hashlib
import socket
import threading

#creates a socket for wireless data transfer, note that all date will need to be encoded to be sent
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999)) #Change to localhost if you dont want to use my server for authentication

server.listen()

def ClientHandeling(c):
    while True:
        NewOrOld = c.recv(1024).decode()

        if NewOrOld == "old":
            #recives the user data
            c.send("Account name: ".encode())
            Username = c.recv(1024).decode()
            c.send("Password: ".encode())
            Password = c.recv(1024)

            Password = hashlib.sha256(Password).hexdigest() #converts password to hash for camparisin against the database

            #connects to the database
            cx = sqlite3.connect("Users.db")
            cu = cx.cursor()

            #compares your input agaist the database
            cu.execute("SELECT * FROM UserData WHERE Username = ? AND Password = ?", (Username, Password))
            if cu.fetchall():
                print("Authentication complete, have plesent stay!")
                #placeholder for account actions
            else:
                print("Authentication failed, please typ again")
        elif NewOrOld == "new":
            #recives the user data for the new account
            c.send("New account name: ".encode())
            NewUsername = c.recv(1024).decode()
            c.send("New password: ".encode())
            NewPassword = c.recv(1024)

            NewPassword = hashlib.sha256(NewPassword).hexdigest() #converts password to hash so that no plain text version is stored

            #connects to the database
            cx = sqlite3.connect("Users.db")
            cu = cx.cursor()

            try:
                cu.execute("INSERT INTO UserData (Username, Password) VALUES (?, ?)", (NewUsername, NewPassword))

                cx.commit()

                print("Account created, please proceed to the login page")
            except:
                print("Account creation failed, please try again")


while True:
    client, addr = server.accept()
    threading.Thread(target=ClientHandeling, args=(client,)).start()
    