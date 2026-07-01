# 🔐 Secure Coding Review Report

**Intern:** Param Parag Koli
**Internship:** CodeAlpha — Cyber Security
**Task:** Task 3 — Secure Coding Review
**Language:** Python
**Application:** User Authentication & Database System

---

## 📋 Executive Summary

A thorough security audit was conducted on a Python-based user authentication and database management application. The review identified **7 critical security vulnerabilities** in the original codebase. Each vulnerability has been documented with its risk level, explanation, and a secure remediation with code examples.

---

## 🔍 Vulnerability Findings

### Vulnerability 1 — SQL Injection
**Severity:** 🔴 CRITICAL

**Location:** `login()`, `get_user_data()`, `display_user_info()` functions

**Vulnerable Code:**
```python
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
cursor.execute(query)
```

**Description:**
User input is directly concatenated into SQL queries without sanitization. An attacker can inject malicious SQL code to bypass authentication, extract all data, or destroy the database.

**Attack Example:**
Username: ' OR '1'='1
Password: anything

This input transforms the query into:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'anything'
```
Since `'1'='1'` is always true, the attacker gains access without valid credentials.

**Secure Fix:**
```python
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
```
Using parameterized queries ensures user input is never interpreted as SQL code.

---

### Vulnerability 2 — Weak Password Hashing (MD5)
**Severity:** 🔴 CRITICAL

**Location:** `hash_password()` function

**Vulnerable Code:**
```python
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
```

**Description:**
MD5 is a cryptographically broken hash function. MD5 hashes can be cracked in seconds using rainbow tables or brute force attacks. Passwords stored as MD5 hashes provide virtually no security.

**Secure Fix:**
```python
def hash_password(password):
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{hashed.hex()}"
```
PBKDF2 with SHA-256 and 100,000 iterations is computationally expensive, making brute force attacks impractical.

---

### Vulnerability 3 — Hardcoded Credentials & Secret Keys
**Severity:** 🔴 CRITICAL

**Location:** Top of file — global variables

**Vulnerable Code:**
```python
SECRET_KEY = "admin123"
ADMIN_PASSWORD = "password123"
```

**Description:**
Hardcoded credentials in source code are a severe security risk. Anyone with access to the codebase (including version control history) can extract these credentials. Weak passwords like "admin123" and "password123" are also trivially guessable.

**Secure Fix:**
```python
SECRET_KEY = secrets.token_hex(32)
```
Use environment variables or secrets managers for sensitive values. Generate cryptographically secure random keys programmatically.

---

### Vulnerability 4 — No Input Validation
**Severity:** 🟠 HIGH

**Location:** All functions accepting user input

**Vulnerable Code:**
```python
def login(username, password):
    # No validation — accepts any input
    query = "SELECT * FROM users WHERE username = '" + username + "'"
```

**Description:**
Without input validation, attackers can submit malformed, excessively long, or specially crafted inputs that cause unexpected behavior, buffer overflows, or injection attacks.

**Secure Fix:**
```python
def validate_input(input_string, max_length=50):
    if not input_string or len(input_string) > max_length:
        return False
    pattern = re.compile(r'^[a-zA-Z0-9_@.]+$')
    return bool(pattern.match(input_string))
```
Always validate input length, type, and format before processing.

---

### Vulnerability 5 — OS Command Injection
**Severity:** 🔴 CRITICAL

**Location:** `execute_command()` function

**Vulnerable Code:**
```python
def execute_command(cmd):
    os.system(cmd)
```

**Description:**
Passing unsanitized user input to `os.system()` allows attackers to execute arbitrary system commands. An attacker could delete files, create backdoors, or take full control of the system.

**Attack Example:**
cmd = "ls; rm -rf /"

**Secure Fix:**
Never pass user input directly to system commands. If OS commands are necessary, use `subprocess` with a list of arguments and avoid shell=True:
```python
import subprocess
subprocess.run(['safe_command', '--arg', value], shell=False)
```

---

### Vulnerability 6 — No Account Lockout Mechanism
**Severity:** 🟠 HIGH

**Location:** `login()` function

**Vulnerable Code:**
```python
def login(username, password):
    # No limit on login attempts
    cursor.execute(query)
```

**Description:**
Without account lockout, attackers can perform unlimited brute force attempts to guess passwords. Given weak passwords like "12345" in the database, this is trivially exploitable.

**Secure Fix:**
```python
cursor.execute("SELECT * FROM users WHERE username = ? AND failed_attempts < 5", (username,))
# Increment failed_attempts on each failed login
cursor.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?", (username,))
```
Lock accounts after 5 failed attempts and implement exponential backoff.

---

### Vulnerability 7 — Sensitive Data Exposure in Logs & Output
**Severity:** 🟠 HIGH

**Location:** `login()`, `display_user_info()` functions

**Vulnerable Code:**
```python
print(f"Executing query: {query}")
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}, Role: {user[3]}")
```

**Description:**
Printing raw SQL queries exposes the application's database structure to attackers. Displaying plaintext passwords in output is a severe data exposure vulnerability.

**Secure Fix:**
```python
# Never print passwords or raw queries
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")
# Use proper logging instead of print statements
logging.info(f"User {username} logged in successfully")
```

---

## 📊 Vulnerability Summary Table

| # | Vulnerability | Severity | Status |
|---|--------------|----------|--------|
| 1 | SQL Injection | 🔴 Critical | ✅ Fixed |
| 2 | Weak Password Hashing (MD5) | 🔴 Critical | ✅ Fixed |
| 3 | Hardcoded Credentials | 🔴 Critical | ✅ Fixed |
| 4 | No Input Validation | 🟠 High | ✅ Fixed |
| 5 | OS Command Injection | 🔴 Critical | ✅ Fixed |
| 6 | No Account Lockout | 🟠 High | ✅ Fixed |
| 7 | Sensitive Data Exposure | 🟠 High | ✅ Fixed |

---

## ✅ Secure Coding Best Practices

1. **Always use parameterized queries** — Never concatenate user input into SQL
2. **Use strong password hashing** — PBKDF2, bcrypt, or Argon2 with salting
3. **Never hardcode secrets** — Use environment variables or secrets managers
4. **Validate all user input** — Check type, length, and format
5. **Implement account lockout** — Prevent brute force attacks
6. **Use least privilege principle** — Only expose necessary data
7. **Enable security logging** — Log all authentication events
8. **Keep dependencies updated** — Patch known vulnerabilities regularly

---

## 🛠️ Tools Used

- **Manual Code Review** — Line by line inspection
- **Python Static Analysis** — Logical flow analysis
- **OWASP Top 10** — Industry standard vulnerability reference
- **CWE Database** — Common Weakness Enumeration reference

---

## 📚 References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE SQL Injection: https://cwe.mitre.org/data/definitions/89.html
- Python Security Best Practices: https://docs.python.org/3/library/secrets.html
- NIST Password Guidelines: https://pages.nist.gov/800-63-3/

---

*Report prepared by Param Parag Koli | CodeAlpha Cyber Security Internship*