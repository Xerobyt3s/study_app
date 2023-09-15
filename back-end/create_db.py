import sqlite3
import hashlib

cx = sqlite3.connect("Data.db")
cu = cx.cursor()

cu.execute("""
CREATE TABLE IF NOT EXISTS UserData (
    id INTEGER PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Permission VARCHAR(255) NOT NULL
)
""")

admin_username, admin_password, admin_permission = "Admin", hashlib.sha256("Admin".encode()).hexdigest(), "Admin" 

cu.execute("INSERT INTO UserData (Username, Password, Permission) VALUES (?, ?, ?)", (admin_username, admin_password, admin_permission))

cx.commit()
