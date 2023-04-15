"""Message Broker"""
import enum
from typing import Dict, List, Any, Tuple
import socket
import selectors

from src.protocol import CDProto
from src.middleware import MiddlewareType as MType

class Serializer(enum.Enum):
    """Possible message serializers."""

    JSON = 0
    XML = 1
    PICKLE = 2


class Broker:
    """Implementation of a PubSub Message Broker."""

    def __init__(self):
        """Initialize broker."""
        self.canceled = False

        self._host = "localhost"
        self._port = 5000
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((self._host, self._port))
        self.sock.listen(10)

        self.sel = selectors.DefaultSelector()

        self.list_topic = {}
        self.list_subscription = []

        # wait register event to accept
        self.sel.register(self.sock, selectors.EVENT_READ, Broker.accept);  

    def list_topics(self) -> List[str]:
        """Returns a list of strings containing all topics containing values."""
        return self.list_topic.keys()

    def get_topic(self, topic):
        """Returns the currently stored value in topic."""
        return self.list_topic.get(topic)


    def put_topic(self, topic, value):
        """Store in topic the value."""
        self.list_topic[topic] = value

    def list_subscriptions(self, topic: str) -> List[Tuple[socket.socket, Serializer]]:
        """Provide list of subscribers to a given topic."""
        ret_list = []
        for element in self.list_subscription:
            if element[0] == topic:
                ret_list.append((element[1], element[2]))
        return ret_list

    def subscribe(self, topic: str, address: socket.socket, _format: Serializer = None):
        """Subscribe to topic by client in address."""
        self.list_subscription.append((topic, address, _format))

    def unsubscribe(self, topic, address):
        """Unsubscribe to topic by client in address."""
        for element in self.list_subscription:
            if(element[0] == topic and element[1] == address):
                break
        print(element)
        self.list_subscription.remove(element)


    # --------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Accept socket
    def accept(self, sock):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, Broker.read)

    # Read user input
    def read(self, conn):
        data = CDProto.recv_msg(conn)

        if data != None:
            msg = data.getMessage()
            
            # Consumer handling
            if msg["type"] == MType.CONSUMER.value:
                
                print("Consumidor: subscribed to",msg["topic"])
                topic = msg["topic"]
                serialize = Serializer(msg["serialize"])
                
                if topic not in self.list_topic:
                    self.put_topic(topic, None)
                    
                self.subscribe(topic, conn, serialize)
                print(self.list_subscriptions(topic))
                value = self.get_topic(topic)
                CDProto.send_msg(conn, value, serialize)
                print('s')             
            
            # Producer handling
            else:
                print("Produtor: send topic to",msg["topic"])
                topic = msg["topic"]
                value = msg["value"]
                self.put_topic(topic, value)
                
                for sub in self.list_subscription:
                    if topic == sub[0]:
                        print('send to',sub[1],msg)
                        msg = CDProto.message(value, topic, MType.CONSUMER.value, sub[2])
                        CDProto.send_msg(sub[1], msg, sub[2])
                        
        else:
            self.sel.unregister(conn)
            conn.close()

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Wait for user event
    def run(self):
        """Run until canceled."""

        while not self.canceled:
            events = self.sel.select();
            for key, mask in events:
                callback = key.data
                callback(self, key.fileobj);
            pass
