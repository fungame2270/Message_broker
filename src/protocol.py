from src.protocols.json_protocol import Json_P
from src.protocols.pickle_protocol import Pickle_P
import json
import pickle
import socket

from src.protocols.Serializer import Serializer

class Message:
    #Message Type.

    def __str__(self):
        if self.serialize == 0:
            return json.dumps(self.getMessage())
        elif self.serialize == 1:
            return pickle.dumps(self.getMessage())
        #elif self.serialize == 2:
        #    return xml.dumps(self.getMessage())
        
    def getMessage(self):
        return self.message
    
class SubscribeMessage(Message):
    #Message to join a topic
    def __init__(self, command, topic, tipo, serialize):
        self.serialize = serialize
        self.message = {"command":command}
        self.message["topic"] = topic
        self.message["type"] = tipo
        self.message["serialize"] = serialize

class UnsubscribeMessage(Message):
    #Message to join a topic
    def __init__(self, command, topic, tipo, serialize):
        self.serialize = serialize
        self.message = {"command":command}
        self.message["topic"] = topic
        self.message["type"] = tipo
        self.message["serialize"] = serialize
    
class TextMessage(Message):
    #Message to chat with other clients.
    def __init__(self, command, message, topic, tipo, serialize):
        self.serialize = serialize
        self.message = {"command":command}
        self.message["value"] = message
        self.message["topic"] = topic
        self.message["type"] = tipo
        self.message["serialize"] = serialize

class CDProto:
    @classmethod
    def subscribe(cls, topic: str, tipo, serialize) -> SubscribeMessage:
        # Creates a JoinMessage object and returns object
        return SubscribeMessage("subscribe", topic, tipo, serialize)

    @classmethod
    def message(cls, value: str, topic: str, tipo: str,serialize) -> TextMessage:
        # Creates a TextMessage object and returns object
        return TextMessage("value", value, topic, tipo, serialize)
    
    @classmethod
    def send_msg(cls, connection: socket, msg: Message, serialize):
        # Choose format
        if serialize == Serializer.JSON.value:
            Json_P.send_msg(connection, msg)
        elif serialize == Serializer.PICKLE.value:
            Pickle_P.send_msg(connection, msg)

    @classmethod
    def recv_msg(cls, connection: socket) -> Message:
        serialize = int.from_bytes(connection.recv(1), 'big')

        if serialize == Serializer.JSON.value:
            message = Json_P.recv_msg(connection)
        elif serialize == Serializer.PICKLE.value:
            message = Pickle_P.recv_msg(connection)

        
       
        if message == None:
            return None

        # selecting message type
        if message["command"] == "subscribe":
            return CDProto.subscribe(message["topic"], message["type"], message["serialize"]);
    
        elif message["command"] == "value":
            return CDProto.message(message["value"], message["topic"], message["type"], message["serialize"])
