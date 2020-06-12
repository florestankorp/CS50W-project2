import json
import os
import re

from flask import Flask, redirect, render_template, request, session, url_for
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

channels = []
global_channel_errors = []

"""
TODO:
* remembering last visited channel after closing and re-opening browser
"""


@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    channel_exists = False

    # check if there is a logged in user
    if "user" in session and not session["user"] == "":
        user = session["user"]
        pass
    else:
        session["user"] = {}
        return redirect("/register")

    # check if referrer is channel to determine if navigation to previous session should be restored
    print(re.search("/channel", request.referrer))
    match = re.search("/channel", request.referrer)

    if not match is None:
        return redirect(url_for("channel", id=user["last_visit"]))

    if request.method == "POST":
        # get and validate form data
        if not request.form.get("channel-name"):
            errors.append("Please provide channel name")
            pass
        else:
            channel_name = request.form.get("channel-name")
            for channel in channels:
                if channel.name == channel_name:
                    channel_exists = True
                    errors.append("Channel already exists")
                    break

            if not channel_exists:
                new_channel = Channel(channel_name, [])
                channels.append(new_channel)

    return render_template("index.html", user=user, channels=channels, errors=errors)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/register")


@app.route("/channel/<int:id>", methods=["GET", "POST"])
def channel(id):
    # check if there is a logged in user
    try:
        user = session["user"]
        pass
    except KeyError:
        session["user"] = {}
        return redirect("/register")

    if not len(channels) > 0:
        return redirect("/")

    for channel in channels:
        if channel.channel_id == id:
            this_channel = channel
            break
        else:
            this_channel = None

    if this_channel is None:
        return redirect("/")

    # remember this channel as the last one visited by the user
    session["user"] = {"name": user["name"], "last_visit": id}

    return render_template(
        "channel.html", errors=global_channel_errors, channel=this_channel
    )


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
            session["user"] = {"name": username}
            return redirect("/")

    return render_template("register.html", errors=errors)


@socketio.on("message sent")
def handle_message(data):
    messages = []

    # check if there is a logged in user
    try:
        user = session["user"]
        pass
    except KeyError:
        session["user"] = {}
        return redirect("/register")

    if data["message"] == "":
        global_channel_errors.append("Please enter a message")
        pass
    else:
        # clear errors array on success
        del global_channel_errors[:]

        # get message from html data attribute through JS
        message = data["message"]

        # get channel_id from html data attribute through JS
        id = int(data["channel_id"])

        for channel in channels:
            if channel.channel_id == id:
                # store only last 100 messages serverside
                if len(channel.messages) >= 100:
                    channel.messages.remove(channel.messages[0])
                    channel.messages.append(Message(user["name"], message))
                    break
                else:
                    channel.messages.append(Message(user["name"], message))
                    break

        # convert Message class instance to object
        # TODO: validate message length
        for message in channel.messages:
            formated_message = message.__dict__
            messages.append(formated_message)

    emit("messages", messages, broadcast=True)
