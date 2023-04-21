"""Middleware to communicate with PubSub Message Broker."""
from collections.abc import Callable
from enum import Enum
from queue import LifoQueue, Empty
from typing import Any

from src.protocol import CDProto
from src.protocols.xml_protocol import Xml_P
from src.protocols.Serializer import Serializer

import socket


class MiddlewareType(Enum):
    """Middleware Type."""

    CONSUMER = 1
    PRODUCER = 2


class Queue:
    """Representation of Queue interface for both Consumers and Producers."""

    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        """Create Queue."""
        self.topic = topic
        self._tipo = _type
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 5000))

    def push(self, value):
        """Sends data to broker."""

    def pull(self) -> (str, Any):
        """Receives (topic, data) from broker.

        Should BLOCK the consumer!"""

    def list_topics(self, callback: Callable):
        #callback funçao a ser chamada qunado lista de topicos vier
        """Lists all topics available in the broker."""

    def cancel(self):
        """Cancel subscription."""


class JSONQueue(Queue):
    """Queue implementation with JSON based serialization."""

    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        super().__init__(topic,_type)
        if _type == MiddlewareType.CONSUMER:
            msg = CDProto.subscribe(topic, _type.value, Serializer.JSON.value)
            CDProto.send_msg(self.sock, msg, Serializer.JSON.value)

    def push(self, value):
        # Producer sends data to broker.
        message = CDProto.message(value, self.topic, self._tipo.value, Serializer.JSON.value)
        CDProto.send_msg(self.sock, message, Serializer.JSON.value)

    def pull(self) -> (str, Any):
        # Consumer receives (topic, data) from broker.
        data = CDProto.recv_msg(self.sock)
        msg = data.getMessage()

        topic = msg["topic"]
        value = msg["value"]
        
        return (topic, value)

    def cancel(self):
        # Cancel subscription
        message = CDProto.unsubscribe(self._tipo.value, Serializer.JSON.value)
        CDProto.send_msg(self.sock, message, Serializer.JSON.value)

class XMLQueue(Queue):
    """Queue implementation with XML based serialization."""

    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        super().__init__(topic,_type)
        if _type == MiddlewareType.CONSUMER:
            msg = Xml_P.subscribe(topic, _type.value, Serializer.XML.value)
            CDProto.send_msg(self.sock, msg, Serializer.XML.value)

    def push(self, value):
        # Producer sends data to broker.
        message = Xml_P.message(value, self.topic, self._tipo.value, Serializer.XML.value)
        CDProto.send_msg(self.sock, message, Serializer.XML.value)
        pass

    def pull(self) -> (str, Any):
        # Consumer receives (topic, data) from broker.
        data = CDProto.recv_msg(self.sock)
        msg = data.getMessage()

        topic = msg["topic"]
        value = msg["value"]

        return (topic, value)

    def cancel(self):
        # Cancel subscription
        message = Xml_P.unsubscribe(self._tipo.value,Serializer.XML.value)
        CDProto.send_msg(self.sock, message, Serializer.XML.value)

class PickleQueue(Queue):
    """Queue implementation with Pickle based serialization."""

    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        super().__init__(topic,_type)
        if _type == MiddlewareType.CONSUMER:
            msg = CDProto.subscribe(topic, _type.value, Serializer.PICKLE.value)
            CDProto.send_msg(self.sock, msg, Serializer.PICKLE.value)

    def push(self, value):
        # Producer sends data to broker.
        message = CDProto.message(value, self.topic, self._tipo.value, Serializer.PICKLE.value)
        CDProto.send_msg(self.sock, message, Serializer.PICKLE.value)
        pass

    def pull(self) -> (str, Any):
        # Consumer receives (topic, data) from broker.
        data = CDProto.recv_msg(self.sock)
        msg = data.getMessage()

        topic = msg["topic"]
        value = msg["value"]

        return (topic, value)

    def cancel(self):
        # Cancel subscription
        message = CDProto.unsubscribe(self._tipo.value,Serializer.PICKLE.value)
        CDProto.send_msg(self.sock, message, Serializer.PICKLE.value)