import pickle
from socket import socket
from src.protocols.CDProtoBadFormat import CDProtoBadFormat
from src.protocols.Serializer import Serializer
        

class Pickle_P:

    @classmethod
    def send_msg(cls, connection: socket, msg):
        #Sends through a connection a Message object.

        serialize = Serializer.PICKLE.value
        serialize = serialize.to_bytes(1, 'big')
        messageToSend = pickle.dumps(msg.getMessage());
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
            return pickle.loads(data)
        except:
            raise CDProtoBadFormat(data)