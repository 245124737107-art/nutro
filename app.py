from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Secret key for session
app.secret_key = "supersecretkey"  # Change this for production

# In-memory user storage (replace with DB in production)
users_db = {}

# ===== Signup =====
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if username in users_db:
        return jsonify({"error": "Username already exists"}), 400

    # Store hashed password
    users_db[username] = generate_password_hash(password)
    return jsonify({"message": "User created successfully!"})

# ===== Login =====
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in users_db or not check_password_hash(users_db[username], password):
        return jsonify({"error": "Invalid username or password"}), 401

    session["user"] = username
    return jsonify({"message": "Login successful", "user": username})

# ===== Check Session =====
@app.route("/check")
def check_login():
    if "user" in session:
        return jsonify({"loggedIn": True, "user": session["user"]})
    return jsonify({"loggedIn": False})

# ===== Logout =====
@app.route("/logout")
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out"})

# ===== Serve Frontend =====
@app.route("/")
def index():
    return open("index.html").read()  # Place your HTML as index.html in the same folder

if __name__ == "__main__":
    app.run(debug=True)
