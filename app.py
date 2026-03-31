from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__)
app.secret_key = "supersecretkey"

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
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
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
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"], role=session["role"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

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
        results = conn.execute("SELECT * FROM patients WHERE full_name LIKE ?", ('%' + query + '%',)).fetchall()
        conn.close()
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)