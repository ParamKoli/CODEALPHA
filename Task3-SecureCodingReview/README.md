# 🔐 Secure Coding Review

**Name:** Param Parag Koli
**Internship:** CodeAlpha — Cyber Security
**Task:** Task 3

## Objective
Perform a code review to identify security vulnerabilities in a Python application, document findings, and provide secure remediation with code examples.

## Files
| File | Description |
|------|-------------|
| `vulnerable_code.py` | Original code with 7 security vulnerabilities |
| `secure_code.py` | Fixed and secured version of the code |
| `security_review_report.md` | Detailed vulnerability report with findings and fixes |

## Tech Stack
Python, SQLite, OWASP Top 10, CWE Database

## Vulnerabilities Found & Fixed
| # | Vulnerability | Severity |
|---|--------------|----------|
| 1 | SQL Injection | 🔴 Critical |
| 2 | Weak Password Hashing (MD5) | 🔴 Critical |
| 3 | Hardcoded Credentials | 🔴 Critical |
| 4 | No Input Validation | 🟠 High |
| 5 | OS Command Injection | 🔴 Critical |
| 6 | No Account Lockout | 🟠 High |
| 7 | Sensitive Data Exposure | 🟠 High |

## Key Takeaways
- Always use parameterized queries to prevent SQL injection
- Use PBKDF2 or bcrypt for password hashing — never MD5
- Never hardcode credentials in source code
- Validate all user input before processing
- Implement account lockout to prevent brute force attacks
