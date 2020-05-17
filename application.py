import os

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_socketio import SocketIO, emit

from channel import Channel, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
channels = [
    Channel(
        "channel 1",
        [
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
        ],
    ),
    Channel(
        "channel 2",
        [
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
        ],
    ),
    Channel(
        "channel 3",
        [
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
        ],
    ),
    Channel(
        "channel 4",
        [
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
            Message("admin1", "001", "yoloooo"),
        ],
    ),
]


@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    # check if there is a logged in user
    try:
        username = session["username"]
        pass
    except KeyError:
        session["username"] = ""
        return redirect("/register")

    return render_template("index.html", username=username, channels=channels)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []
    if request.method == "POST":
        # get and validate form data
        if not request.form.get("username"):
            errors.append("Please enter a username")
            pass
        else:
            username = request.form.get("username")
            session["username"] = username
            return redirect("/")

    return render_template("register.html", errors=errors)
