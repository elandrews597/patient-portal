import database
from werkzeug.security import generate_password_hash
import os
import subprocess

# Delete existing database if it exists
if os.path.exists("portal.db"):
    os.remove("portal.db")

# Create fresh database
database.init_db()

# Check which branch we're on
branch = subprocess.check_output(["git", "branch", "--show-current"]).decode().strip()

conn = database.get_db()

if branch == "hardened-version":
    # Hardened version uses hashed passwords
    conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ('testuser', generate_password_hash('password123'), 'patient'))
    conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ('admin', generate_password_hash('admin123'), 'admin'))
    print("Hardened database created with hashed passwords!")
else:
    # Vulnerable version uses plain text passwords
    conn.execute("INSERT INTO users (username, password, role) VALUES ('testuser', 'password123', 'patient')")
    conn.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    conn.execute("INSERT INTO users (username, password, role) VALUES ('jackball', 'password345', 'patient')")
    conn.execute("INSERT INTO users (username, password, role) VALUES ('bigjane', 'bigjane123', 'patient')")
    print("Vulnerable database created with plain text passwords!")

# Add sample patients (same for both branches)
conn.execute("INSERT INTO patients (user_id, full_name, date_of_birth, diagnosis, notes) VALUES (1, 'John Doe', '1990-05-15', 'Hypertension', 'Patient needs monthly checkups')")
conn.execute("INSERT INTO patients (user_id, full_name, date_of_birth, diagnosis, notes) VALUES (3, 'Jack Ball', '1980-05-09', 'Back Pain', 'Has a lot of back pain, needs help')")
conn.execute("INSERT INTO patients (user_id, full_name, date_of_birth, diagnosis, notes) VALUES (4, 'Big Jane', '1976-07-12', 'Blanching rash', 'HR: 95 regular BP: 70/35 Temp: 40.1C/104.2F RR: 9 O2 Sat: 92% on RA History: Drunk')")


conn.commit()
conn.close()
print("Sample patients added!")