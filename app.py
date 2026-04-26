from logging import exception
# added the flask limiter imports
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask import Flask, render_template, request, redirect, url_for, session, make_response
# added hash import from werkzeug security
from werkzeug.security import generate_password_hash, check_password_hash

import database
# removed unnecessary imports

app = Flask(__name__)
app.secret_key = "8f42a73054b1749f8f58848be5e6502c"
# impplemented limiter; tracks IP address, sets limits per day
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        conn = database.get_db()
        # Password is now hashed using werkzeug before storing
        # Parameterized query (?) prevents SQL injection 
        # Error handling added to catch duplicate username and other database errors
        try:
            conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'patient')", (username, hashed_password))
            conn.commit()
        except Exception as e:
            print(e)
            return render_template("error.html", error="Username already exists. Please choose a different one.")
        finally:
            conn.close()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
# implemented number of logins per minute
@limiter.limit("10 per minute")
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = database.get_db()
        # Used parameterized query to prevent SQL injection authentication bypass
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        # Password is verified against has by comparing hashes using check_password_hash
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/dashboard")
#replaced sess = get_session() and all sess[] with Flask's built in session
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"], role=session["role"])


@app.route("/logout")
def logout():
    # FIXED: Using Flask's session.clear() instead of custom cookie deletion
    session.clear()
    return redirect(url_for("index"))

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/record", methods=["GET", "POST"])
def record():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        full_name = request.form["full_name"]
        date_of_birth = request.form["date_of_birth"]
        diagnosis = request.form["diagnosis"]
        notes = request.form["notes"]
        conn = database.get_db()
        # Used parameterized query to prevent SQL injection(?)
        conn.execute("INSERT INTO patients (user_id, full_name, date_of_birth, diagnosis, notes) VALUES (?, ?, ?, ?, ?)", (session["user_id"], full_name, date_of_birth, diagnosis, notes))
        conn.commit()
        conn.close()
        return render_template("record.html", success="Record added successfully!")
    return render_template("record.html")

@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "admin":
        return redirect(url_for("dashboard"))
    conn = database.get_db()
    records = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()
    return render_template("admin.html", records=records)

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user_id" not in session:
        return redirect(url_for("login"))
    results = []
    if request.method == "POST":
        query = request.form["query"]
        conn = database.get_db()
        # parameterized query prevents SQL injection(?)
        # User input is treated as data, not SQL code (' OR '1'='1 will pass as a string not SQL code)
        results = conn.execute("SELECT * FROM patients WHERE full_name LIKE ?", ('%' + query + '%',)).fetchall()
        conn.close()
    return render_template("search.html", results=results)

# Disabled debug mode and set a single host
if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)