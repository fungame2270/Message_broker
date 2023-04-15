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
    
class SubscribeMessage(Message):
    #Message to join a topic channe
    def __init__(self, command, topic, tipo,queue):
        self.message = {"command":command}
        self.message["topic"] = topic
        self.message["type"] = tipo
        self.message["queue"] = queue

class RegisterMessage(Message):
    #Message to register username in the server.
    def __init__(self, command, user):
        self.message = {"command":command}
        self.message["user"] = user
    
class TextMessage(Message):
    #Message to chat with other clients.
    def __init__(self, command, message, topic, tipo):
        self.message = {"command":command}
        self.message["value"] = message
        self.message["topic"] = topic
        self.message["type"] = tipo
        

class CDProto:
    #Computação Distribuida Protocol.

    @classmethod
    def register(cls, username: str) -> RegisterMessage:
        # Creates a RegisterMessage object and returns object
        return RegisterMessage("register", username)

    @classmethod
    def subscribe(cls, topic: str, tipo,queue) -> SubscribeMessage:
        # Creates a JoinMessage object and returns object
        return SubscribeMessage("subscribe", topic, tipo,queue)

    @classmethod
    def message(cls, value: str, topic: str, tipo: str) -> TextMessage:
        # Creates a TextMessage object and returns object
        return TextMessage("value", value, topic, tipo)

    @classmethod
    def send_msg(cls, connection: socket, msg: Message):
        #Sends through a connection a Message object.

        messageToSend = json.dumps(msg.getMessage());
        messageSize = len(messageToSend.encode());

        byteMessage = messageSize.to_bytes(2, 'big');
        connection.sendall(byteMessage + messageToSend.encode())

    @classmethod
    def recv_msg(cls, connection: socket) -> Message:
        #Receives through a connection a Message object.

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
    
        elif message["command"] == "subscribe":
            return CDProto.subscribe(message["topic"], message["type"],message["queue"]);
    
        elif message["command"] == "value":
            return CDProto.message(message["value"], message["topic"], message["type"])


class CDProtoBadFormat(Exception):
    #Exception when source message is not CDProto.

    def __init__(self, original_msg: bytes=None) :
        #Store original message that triggered exception.
        self._original = original_msg

    @property
    def original_msg(self) -> str:
        #Retrieve original message as a string.
        return self._original.decode("utf-8")
