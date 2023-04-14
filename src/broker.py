"""Message Broker"""
import enum
from typing import Dict, List, Any, Tuple
import socket
import selectors

from json_protocol import CDProto

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

        self.sel = selectors.DefaultSelector()

        self.list_topic = {}
        self.list_subscription = []

        # wait register event to accept
        self.sel.register(self.serversock, selectors.EVENT_READ, Broker.accept);  

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



    def accept(self, sock):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, Broker.read)

    def read(self, conn):
        data = CDProto.recv_msg(conn)
        if data:
            print("existe algo")
        else:
            self.sel.unregister(conn)
            conn.close()

    def run(self):
        """Run until canceled."""

        while not self.canceled:
            events = self.sel.select();
            for key, mask in events:
                callback = key.data
                callback(self, key.fileobj);
            pass
