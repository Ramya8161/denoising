from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import cv2

from model import process_image

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
RESULT_FOLDER = os.path.join(BASE_DIR, "static/results")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

print("DB PATH:", DB_PATH)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect(url_for("login"))

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        print("REGISTER INPUT:", username, password)

        if not username or not password:
            return "Fields cannot be empty!"

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        # VERIFY INSERT
        c.execute("SELECT * FROM users")
        print("AFTER INSERT:", c.fetchall())

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        print("LOGIN INPUT:", username, password)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("SELECT username, password FROM users")
        users = c.fetchall()

        print("DB USERS:", users)

        conn.close()

        # MANUAL MATCH (NO SQL BUGS)
        for u, p in users:
            if u == username and p == password:
                session["user"] = username
                return redirect(url_for("upload"))

        return "Invalid Credentials!"

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ---------------- DEBUG ROUTE ----------------
@app.route("/debug")
def debug():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    data = c.fetchall()

    conn.close()

    return str(data)

# ---------------- UPLOAD ----------------
@app.route("/upload")
def upload():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("upload.html")

# ---------------- PROCESS IMAGE ----------------
@app.route("/process", methods=["POST"])
def process():
    if "user" not in session:
        return redirect(url_for("login"))

    if "image" not in request.files:
        return "No file uploaded!"

    file = request.files["image"]

    if file.filename == "":
        return "No selected file!"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    original, wiener_img, bm3d_img = process_image(filepath)

    cv2.imwrite(os.path.join(RESULT_FOLDER, "wiener.png"), wiener_img * 255)
    cv2.imwrite(os.path.join(RESULT_FOLDER, "bm3d.png"), bm3d_img * 255)

    return render_template(
        "result.html",
        original=filepath,
        wiener="results/wiener.png",
        bm3d="results/bm3d.png"
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()