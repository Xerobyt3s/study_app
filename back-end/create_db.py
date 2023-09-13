import sqlite3
import hashlib

cx = sqlite3.connect("Users.db")
cu = cx.cursor()

cu.execute("""
CREATE TABLE IF NOT EXISTS UserData (
    id INTEGER PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
)
""")

admin_username, admin_password = "Admin", hashlib.sha256("Admin".encode()).hexdigest() 

cu.execute("INSERT INTO UserData (Username, Password) VALUES (?, ?)", (admin_username, admin_password))

cx.commit()
