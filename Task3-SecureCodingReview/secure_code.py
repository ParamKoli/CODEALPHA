import sqlite3
import hashlib
import os
import secrets
import logging
import re

logging.basicConfig(filename='security.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

DATABASE = "users_secure.db"
SECRET_KEY = secrets.token_hex(32)

def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT UNIQUE, 
                      password TEXT, role TEXT, failed_attempts INTEGER DEFAULT 0)''')
    admin_password = hash_password("StrongP@ssw0rd!")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', ?, 'admin', 0)",
                   (admin_password,))
    conn.commit()
    conn.close()

def hash_password(password):
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{hashed.hex()}"

def verify_password(stored_password, provided_password):
    salt, hashed = stored_password.split(':')
    new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt.encode(), 100000)
    return hashed == new_hash.hex()

def validate_input(input_string, max_length=50):
    if not input_string or len(input_string) > max_length:
        return False
    pattern = re.compile(r'^[a-zA-Z0-9_@.]+$')
    return bool(pattern.match(input_string))

def login(username, password):
    if not validate_input(username) or not validate_input(password, 100):
        logging.warning(f"Invalid input attempt for username: {username}")
        print("Invalid input detected!")
        return False

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND failed_attempts < 5",
                   (username,))
    user = cursor.fetchone()

    if user and verify_password(user[2], password):
        cursor.execute("UPDATE users SET failed_attempts = 0 WHERE username = ?",
                       (username,))
        conn.commit()
        conn.close()
        logging.info(f"Successful login for user: {username}")
        print(f"Welcome {user[1]}! Role: {user[3]}")
        return True
    else:
        if user:
            cursor.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?",
                           (username,))
            conn.commit()
        conn.close()
        logging.warning(f"Failed login attempt for username: {username}")
        print("Invalid credentials!")
        return False

def get_user_data(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        logging.warning(f"Invalid user_id: {user_id}")
        return None

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def save_file(filename, data):
    safe_filename = os.path.basename(filename)
    allowed_extensions = ['.txt', '.log', '.csv']
    if not any(safe_filename.endswith(ext) for ext in allowed_extensions):
        logging.warning(f"Blocked attempt to save file with unsafe extension: {filename}")
        print("File type not allowed!")
        return False
    safe_path = os.path.join('/safe/directory', safe_filename)
    with open(safe_path, 'w') as f:
        f.write(data)
    logging.info(f"File saved: {safe_filename}")
    return True

def display_user_info(username):
    if not validate_input(username):
        print("Invalid username!")
        return
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE username = ?", (username,))
    users = cursor.fetchall()
    conn.close()
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")

if __name__ == "__main__":
    create_db()
    print("=== Testing Secure Code ===\n")
    print("Test 1 — Normal Login:")
    login("admin", "StrongP@ssw0rd!")
    print("\nTest 2 — SQL Injection Attempt (blocked):")
    login("' OR '1'='1", "anything")
    print("\nTest 3 — Display User Info:")
    display_user_info("admin")