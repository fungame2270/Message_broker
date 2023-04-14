"""Protocol for chat server - Computação Distribuida Assignment 1."""
import json
from datetime import datetime
from socket import socket

class Message:
    #Message Type.

    def __str__(self):
        return json.dumps(self.getMessage())

    def getMessage(self):
        return self.message
    
class JoinMessage(Message):
    #Message to join a chat channel.
    def __init__(self, command, channel):
        self.message = {"command":command};
        self.message["channel"] = channel;

class RegisterMessage(Message):
    #Message to register username in the server.
    def __init__(self, command, user):
        self.message = {"command":command};
        self.message["user"] = user;
    
class TextMessage(Message):
    #Message to chat with other clients.
    def __init__(self, command, message, channel, ts):
        self.message = {"command":command};
        self.message["message"] = message;
        # if omitted then we have to not include it (due to number of parameters)
        if channel is not None:
            self.message["channel"] = channel;
        self.message["ts"] = ts;

class CDProto:
    #Computação Distribuida Protocol.

    @classmethod
    def register(cls, username: str) -> RegisterMessage:
        # Creates a RegisterMessage object and returns object
        return RegisterMessage("register", username);

    @classmethod
    def join(cls, channel: str) -> JoinMessage:
        # Creates a JoinMessage object and returns object
        return JoinMessage("join", channel)

    @classmethod
    def message(cls, message: str, channel: str = None) -> TextMessage:
        # Creates a TextMessage object and returns object
        return TextMessage("message", message, channel, int(datetime.now().timestamp()))

    @classmethod
    def send_msg(cls, connection: socket, msg: Message):
        #Sends through a connection a Message object.

        # when sending a message, we first send the size of the string
        # and to do so, we use 2 bytes
        # converting the size from decimal to binary and then to 16 bits
        # também podemos utilizar o ASCII

        messageToSend = json.dumps(msg.getMessage());
        messageSize = len(messageToSend.encode());

        # l = 34
        # arr = l.to_bytes(length = 2, byteorder = 'big')
        byteMessage = messageSize.to_bytes(2, 'big');
        connection.sendall(byteMessage + messageToSend.encode())

    @classmethod
    def recv_msg(cls, connection: socket) -> Message:
        #Receives through a connection a Message object.

        # b = int.from_bytes(arr, byteorder = 'big')
        messageSize = int.from_bytes(connection.recv(2), 'big')
        
        if messageSize == 0:
            return

        try:
            data = connection.recv(messageSize)
            message = json.loads(data.decode())
        except:
            raise CDProtoBadFormat(data)

        # selecting message type
        if message["command"] == "register":
            return CDProto.register(message["user"]);
    
        elif message["command"] == "join":
            return CDProto.join(message["channel"]);
    
        elif message["command"] == "message":
            if "channel" in message:
                return CDProto.message(message["message"], message["channel"]);
            else:
                return CDProto.message(message["message"])


class CDProtoBadFormat(Exception):
    #Exception when source message is not CDProto.

    def __init__(self, original_msg: bytes=None) :
        #Store original message that triggered exception.
        self._original = original_msg

    @property
    def original_msg(self) -> str:
        #Retrieve original message as a string.
        return self._original.decode("utf-8")
