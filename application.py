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
            new_channel = Channel(channel_name, [])
            channels.append(new_channel)

    return render_template(
        "index.html", username=username, channels=channels, errors=errors
    )


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/register")


@app.route("/channel/<int:id>", methods=["GET", "POST"])
def channel(id):
    errors = []
    if not len(channels) > 0:
        return redirect("/index")

    for channel in channels:
        if channel.channel_id == id:
            this_channel = channel
            break
        # else:
        #     return redirect("/index")
    print(this_channel.messages)
    return render_template("channel.html", errors=errors, channel=this_channel)


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


@socketio.on("message sent")
def handle_message(data):
    # check if there is a logged in user
    try:
        username = session["username"]
        pass
    except KeyError:
        session["username"] = ""
        return redirect("/register")

    message = data["message"]
    id = int(data["channel_id"])

    for channel in channels:
        if channel.channel_id == id:
            channel.messages.append(Message(username, message))
            break


# @socketio.on("submit vote")
# def vote(data):
#     selection = data["selection"]
#     votes[selection] += 1
#     emit("vote totals", votes, broadcast=True)
#     print(data)
