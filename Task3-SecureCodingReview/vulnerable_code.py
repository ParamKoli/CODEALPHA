import sqlite3
import hashlib
import os

SECRET_KEY = "admin123"
DATABASE = "users.db"
ADMIN_PASSWORD = "password123"

def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'john', '12345', 'user')")
    conn.commit()
    conn.close()

def login(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    print(f"Executing query: {query}")
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    if user:
        print(f"Welcome {user[1]}! Your role is {user[3]}")
        return True
    else:
        print("Login failed!")
        return False

def get_user_data(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def save_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)
    print(f"File saved: {filename}")

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def execute_command(cmd):
    os.system(cmd)

def display_user_info(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}, Role: {user[3]}")

if __name__ == "__main__":
    create_db()
    print("=== Testing Vulnerable Code ===\n")
    print("Test 1 — Normal Login:")
    login("admin", "password123")
    print("\nTest 2 — SQL Injection Attack:")
    login("' OR '1'='1", "anything")
    print("\nTest 3 — Display User Info:")
    display_user_info("admin")