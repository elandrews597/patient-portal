from flask import Flask, render_template, request, redirect, url_for, session
# added hash import from werkzeug security
from werkzeug.security import generate_password_hash, check_password_hash

import database
import json
import base64

app = Flask(__name__)

def get_session():
    cookie = request.cookies.get("session_data")
    if cookie:
        try:
            decoded = base64.b64decode(cookie).decode("utf-8")
            return json.loads(decoded)
        except Exception:
            return {}
    return {}

def set_session(response, data):
    encoded = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    response.set_cookie("session_data", encoded)
    return response

def clear_session(response):
    response.delete_cookie("session_data")
    return response

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
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'patient')", (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
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
def dashboard():
    sess = get_session()
    if "user_id" not in sess:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=sess["username"], role=sess["role"])

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("index")))
    clear_session(response)
    return response

@app.route("/record", methods=["GET", "POST"])
def record():
    sess = get_session()
    if "user_id" not in sess:
        return redirect(url_for("login"))
    if request.method == "POST":
        full_name = request.form["full_name"]
        date_of_birth = request.form["date_of_birth"]
        diagnosis = request.form["diagnosis"]
        notes = request.form["notes"]
        conn = database.get_db()
        # Used parameterized query to prevent SQL injection
        conn.execute("INSERT INTO patients (user_id, full_name, date_of_birth, diagnosis, notes) VALUES (?, ?, ?, ?, ?)", (session["user_id"], full_name, date_of_birth, diagnosis, notes))
        conn.commit()
        conn.close()
        return render_template("record.html", success="Record added successfully!")
    return render_template("record.html")

@app.route("/admin")
def admin():
    sess = get_session()
    if "user_id" not in sess:
        return redirect(url_for("login"))
    if sess["role"] != "admin":
        return redirect(url_for("dashboard"))
    conn = database.get_db()
    records = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()
    return render_template("admin.html", records=records)

@app.route("/search", methods=["GET", "POST"])
def search():
    sess = get_session()
    if "user_id" not in sess:
        return redirect(url_for("login"))
    results = []
    if request.method == "POST":
        query = request.form["query"]
        conn = database.get_db()
        # parameterized query prevents SQL injection
        # User input is treated as data, not SQL code (' OR '1'='1 will pass as a string not SQL code)
        results = conn.execute("SELECT * FROM patients WHERE full_name LIKE ?", ('%' + query + '%',)).fetchall()
        conn.close()
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)