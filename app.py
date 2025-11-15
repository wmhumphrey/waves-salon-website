import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD")

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            # optional: remember where they tried to go
            next_url = request.path
            return redirect(url_for("login", next=next_url))
        return f(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        if password == app.config["ADMIN_PASSWORD"]:
            session["logged_in"] = True
            # go back to the page they wanted, or home
            next_url = request.args.get("next") or url_for("home")
            return redirect(next_url)
        else:
            error = "Incorrect password."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Make {{ year }} available in all templates
@app.route("/")
@login_required
def home():
    return render_template("index.html", active_page="home")

@app.route("/services")
@login_required
def services():
    return render_template("services.html", active_page="services")

@app.route("/gallery")
@login_required
def gallery():
    return render_template("gallery.html", active_page="gallery")

@app.route("/about")
@login_required
def about():
    return render_template("about.html", active_page="about")

@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html", active_page="contact")


if __name__ == "__main__":
    app.run(debug=True)
