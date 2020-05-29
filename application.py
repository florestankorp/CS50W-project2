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
    # Channel(
    #     "channel 1",
    #     [
    #         Message("admin1", "001", "yoloooo"),
    #         Message("admin1", "001", "yoloooo"),
    #         Message("admin1", "001", "yoloooo"),
    #         Message("admin1", "001", "yoloooo"),
    #         Message("admin1", "001", "yoloooo"),
    #         Message("admin1", "001", "yoloooo"),
    #         Message("admin1", "001", "yoloooo"),
    #         Message("admin1", "001", "yoloooo"),
    #     ],
    # ),
]


@app.route("/index", methods=["GET", "POST"])
def index():
    errors = []
    # check if there is a logged in user
    try:
        username = session["username"]
        pass
    except KeyError:
        session["username"] = ""
        return redirect("/register")

    if request.method == "POST":
        # get and validate form data
        if not request.form.get("channel-name"):
            errors.append("Please provide channel name")
            pass
        else:
            channel_name = request.form.get("channel-name")
            channels.append(Channel(channel_name, []))

    return render_template(
        "index.html", username=username, channels=channels, errors=errors
    )


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
            return redirect("/index")

    return render_template("register.html", errors=errors)
