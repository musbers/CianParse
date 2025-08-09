from flask import Flask, send_from_directory, request, redirect, url_for
from config import PASSWORD, MEGA_TABLE, BASE_DIR

app = Flask(__name__)

@app.route("/")
def index():
    if request.cookies.get("auth") == PASSWORD:
        return send_from_directory(BASE_DIR / "frontend", "index.html")
    return """
    <form method='POST' action='/login'>
        <input name='password' type='password'>
        <button>Войти</button>
    </form>
    """

@app.route("/login", methods=["POST"])
def login():
    if request.form.get("password") == PASSWORD:
        resp = redirect(url_for("index"))
        resp.set_cookie("auth", PASSWORD)
        return resp
    return "Неверный пароль", 403

@app.route("/mega_table.csv")
def mega_table():
    if request.cookies.get("auth") == PASSWORD:
        return send_from_directory(MEGA_TABLE.parent, MEGA_TABLE.name)
    return "Unauthorized", 403

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(BASE_DIR / "frontend", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

# python backend/app.py