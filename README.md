# Patient Portal - CSC 2362 Build, Break, Fix Project

## Overview
A simulated Electronic Health Record (EHR) web application built for CSC 2362: Introduction to Cybersecurity and Cyber Defense. This project demonstrates the full DevSecOps cycle — building a functional web app, exploiting its vulnerabilities, and hardening it against attacks.

## Authors
- Elaina Andrews
- Owen Gaspard
- Jaxon Svec

## Tech Stack
- **Backend:** Python + Flask
- **Database:** SQLite
- **Frontend:** HTML
- **Version Control:** Git + GitHub

## Repository Structure
- `vulnerable-version` — the insecure version of the app used for exploitation
- `hardened-version` — the patched and hardened version of the app

## Vulnerabilities Demonstrated
| # | Attack | OWASP 2025 Category |
|---|---|---|
| 1 | SQL Injection | A05 - Injection |
| 2 | Cross-Site Scripting (XSS) | A05 - Injection |
| 3 | Dictionary/Brute Force Attack | A07 - Authentication Failures |
| 4 | Cookie Manipulation | A01 - Broken Access Control |
| 5 | Debug Mode Integrity | A10 - Mishandling of Exceptional Conditions |
| 6 | Denial of Service | A10 - Mishandling of Exceptional Conditions |
| 7 | Cross-Site Request Forgery (CSRF) | A01 - Broken Access Control |
| 8 | Insecure Direct Object Reference (IDOR) | A01 - Broken Access Control |

## Running the App
### Step 1: Clone the repository
git clone https://github.com/elandrews597/patient-portal.git
cd patient-portal
### Step 2: Switch to the desired branch
git checkout vulnerable-version
or
git checkout hardened-version
### Step 3: Install dependencies
pip3 install flask werkzeug
### Step 4: Initialize the database
python3 -c "import database; database.init_db()"
### Step 5: Run the app
python3 app.py
```

Then open your browser and go to: http://localhost:5000
```
## Security Notes
This application was intentionally built with vulnerabilities for educational purposes. The `vulnerable-version` branch should **never** be deployed in a production environment.
