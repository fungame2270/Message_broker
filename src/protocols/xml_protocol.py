import xml.etree.ElementTree as xml
from socket import socket
from src.protocols.CDProtoBadFormat import CDProtoBadFormat
from src.protocols.Serializer import Serializer
        
class Message:
    #Message Type.
    @classmethod
    def xmlStringtoDict(cls,string):
        mark = xml.fromstring(string)
        msg = {}
        for child in mark:
            msg[child.tag] = child.text
        return msg

    def __str__(self):
       return xml.tostring(self.msg).decode() 
        
    def getXml(self):
        return self.msg
    
class SubscribeMessage(Message):
    #Message to join a topic
    def __init__(self, command, topic, tipo, serialize):
        self.serialize = serialize
        self.msg = xml.Element("msg")
        child = xml.SubElement(self.msg, "command")
        child.text = command
        child = xml.SubElement(self.msg, "topic")
        child.text = topic
        child = xml.SubElement(self.msg, "type")
        child.text = str(tipo)
        child = xml.SubElement(self.msg, "serialize")
        child.text = str(serialize)

class UnsubscribeMessage(Message):
    #Message to unjoin a topic
    def __init__(self, command, tipo, serialize, topic):
        self.serialize = serialize
        self.msg = xml.Element("msg")
        child = xml.SubElement(self.msg, "command")
        child.text = command
        child = xml.SubElement(self.msg, "type")
        child.text = str(tipo)
        child = xml.SubElement(self.msg, "serialize")
        child.text = str(serialize)
        child = xml.SubElement(self.msg, "topic")
        child.text = topic       
    
class TextMessage(Message):
    #Message to chat with other clients.
    def __init__(self, command, value, topic, tipo, serialize):
        self.serialize = serialize
        self.msg = xml.Element("msg")
        child = xml.SubElement(self.msg, "command")
        child.text = command
        child = xml.SubElement(self.msg, "value")
        child.text = str(value)
        child = xml.SubElement(self.msg, "topic")
        child.text = topic
        child = xml.SubElement(self.msg, "type")
        child.text = str(tipo)
        child = xml.SubElement(self.msg, "serialize")
        child.text = str(serialize)
    
    def getXml(self):
        return self.msg

class Xml_P:
    @classmethod
    def subscribe(cls, topic: str, tipo, serialize) -> SubscribeMessage:
        # Creates a JoinMessage object and returns object
        return SubscribeMessage("subscribe", topic, tipo, serialize)
    
    @classmethod
    def unsubscribe(cls, tipo, serialize, topic) -> UnsubscribeMessage:
        # Create a UnsubscribeMessage object and returns object 
        return UnsubscribeMessage("unsubscribe", tipo, serialize, topic)

    @classmethod
    def message(cls, value: str, topic: str, tipo: str,serialize) -> TextMessage:
        # Creates a TextMessage object and returns object
        return TextMessage("value", value, topic, tipo, serialize)


    @classmethod
    def send_msg(cls, connection: socket, msg: Message):
        #Sends through a connection a Message object.
        serialize = Serializer.XML.value
        serialize = serialize.to_bytes(1, 'big')
        messageToSend = xml.tostring(msg.getXml())
        messageSize = len(messageToSend)

        byteMessage = messageSize.to_bytes(2, 'big');
        connection.send(serialize + byteMessage + messageToSend)

    @classmethod
    def recv_msg(cls, connection: socket):
        #Receives through a connection a Message object.

        messageSize = int.from_bytes(connection.recv(2), 'big')
        
        if messageSize == 0:
            return

        try:
            data = connection.recv(messageSize)
            dictionary = Message.xmlStringtoDict(data.decode())
            return dictionary
        except:
            raise CDProtoBadFormat(data)