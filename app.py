from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
db = SQL("sqlite:///user.db")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if password != confirm:
            return "password and confirmation are not match"
        elif not password:
            return "password  is required"
        elif not username:
            return " name is required"
        elif rows:
            return "user name already taken"
        else:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", username, generate_password_hash(password)
            )
            rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )
            session["user_id"] = rows[0]["id"]
            return redirect("/")

    else:
        return render_template("register.html")
#end of reigster
