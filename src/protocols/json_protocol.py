import json
from socket import socket
from src.protocols.CDProtoBadFormat import CDProtoBadFormat
from src.protocols.Serializer import Serializer


class Json_P:

    @classmethod
    def send_msg(cls, connection: socket, msg):
        #Sends through a connection a Message object.

        serialize = Serializer.JSON.value
        serialize = serialize.to_bytes(1, 'big')
        messageToSend = json.dumps(msg.getMessage());
        messageSize = len(messageToSend.encode());

        byteMessage = messageSize.to_bytes(2, 'big');
        connection.sendall(serialize + byteMessage + messageToSend.encode())

    @classmethod
    def recv_msg(cls, connection: socket):
        #Receives through a connection a Message object.

        messageSize = int.from_bytes(connection.recv(2), 'big')
        
        if messageSize == 0:
            return

        try:
            data = connection.recv(messageSize)
            return json.loads(data.decode())
        except:
            raise CDProtoBadFormat(data)


