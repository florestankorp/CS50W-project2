import datetime

datetime.date.today()


class Channel:
    def __init__(self, name, messages):
        self.channel_id = id(self)
        self.name = name
        self.messages = messages


class Message:
    def __init__(self, username, content):
        self.username = username
        self.timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
        self.content = content


# channels = [
#     {
#         channelname: "channel 1",
#         messages: [
#             {username: "admin1", timestamp: "000001", message: "Hello World"},
#             {username: "admin2", timestamp: "000002", message: "Hello Mike"},
#             {username: "admin3", timestamp: "000003", message: "Hello Alpha"},
#             {username: "admin4", timestamp: "000004", message: "Hello Bravo"},
#             {username: "admin5", timestamp: "000005", message: "Hello Charlie"},
#             {username: "admin6", timestamp: "000006", message: "Hello Delta"},
#         ],
#     },
#     {
#         channelname: "channel 2",
#         messages: [
#             {username: "admin1", timestamp: "000001", message: "Hello World"},
#             {username: "admin2", timestamp: "000002", message: "Hello Mike"},
#             {username: "admin3", timestamp: "000003", message: "Hello Alpha"},
#             {username: "admin4", timestamp: "000004", message: "Hello Bravo"},
#             {username: "admin5", timestamp: "000005", message: "Hello Charlie"},
#             {username: "admin6", timestamp: "000006", message: "Hello Delta"},
#         ],
#     },
# ]
