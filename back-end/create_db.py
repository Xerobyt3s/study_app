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

cu.execute("""
CREATE TABLE IF NOT EXISTS Definitions (
    id INTEGER PRIMARY KEY,
    Word VARCHAR(255) NOT NULL,
    Definition VARCHAR(255) NOT NULL,
    Subject VARCHAR(255) NOT NULL,
    Author VARCHAR(255) NOT NULL,
    EditDate VARCHAR(255) NOT NULL
)
""")


admin_username, admin_password, admin_permission = "Admin", hashlib.sha256("Admin".encode()).hexdigest(), "Admin" 

cu.execute("SELECT * FROM UserData WHERE Username = ?", (admin_username,)) #note the use of whitelist to stop sql injections
if not cu.fetchall():
    #if the user does not exist, creates the user
    cu.execute("INSERT INTO UserData (Username, Password, Permission) VALUES (?, ?, ?)", (admin_username, admin_password, admin_permission))

cx.commit()
