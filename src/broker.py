"""Message Broker"""
import enum
from typing import Dict, List, Any, Tuple


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

    def list_topics(self) -> List[str]:
        """Returns a list of strings containing all topics containing values."""

    def get_topic(self, topic):
        """Returns the currently stored value in topic."""

    def put_topic(self, topic, value):
        """Store in topic the value."""

    def list_subscriptions(self, topic: str) -> List[Tuple[socket.socket, Serializer]]:
        """Provide list of subscribers to a given topic."""

    def subscribe(self, topic: str, address: socket.socket, _format: Serializer = None):
        """Subscribe to topic by client in address."""

    def unsubscribe(self, topic, address):
        """Unsubscribe to topic by client in address."""

    def run(self):
        """Run until canceled."""

        while not self.canceled:
            pass
