"""Message Broker"""
import enum
from typing import Dict, List, Any, Tuple
import socket
import selectors


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
        self.sock.bind((self._host,self._port))
        self.sock.listen(10)

        #self.sel = selectors.DefaultSelector()

        self.list_topics = {}
        self.list_subscriptions = []

    def list_topics(self) -> List[str]:
        """Returns a list of strings containing all topics containing values."""
        return self.list_topics.keys()

    def get_topic(self, topic):
        """Returns the currently stored value in topic."""
        return self.list_topics.get(topic)


    def put_topic(self, topic, value):
        """Store in topic the value."""
        self.list_topics[topic] = value

    def list_subscriptions(self, topic: str) -> List[Tuple[socket.socket, Serializer]]:
        """Provide list of subscribers to a given topic."""
        ret_list = []
        for element in self.list_subscriptions:
            if element(2) == topic:
                ret_list.append((element(0),element(1)))
        return ret_list

    def subscribe(self, topic: str, address: socket.socket, _format: Serializer = None):
        """Subscribe to topic by client in address."""
        self.list_subscriptions.append((address,Serializer,topic))

    def unsubscribe(self, topic, address):
        """Unsubscribe to topic by client in address."""
        for element in self.list_subscriptions:
            if(element(0) == address and element(2) == topic):
                break
        self.list_subscriptions.pop(element)

    def run(self):
        """Run until canceled."""

        while not self.canceled:
            
            pass
