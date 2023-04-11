"""Middleware to communicate with PubSub Message Broker."""
from collections.abc import Callable
from enum import Enum
from queue import LifoQueue, Empty
from typing import Any


class MiddlewareType(Enum):
    """Middleware Type."""

    CONSUMER = 1
    PRODUCER = 2


class Queue:
    """Representation of Queue interface for both Consumers and Producers."""

    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        """Create Queue."""

    def push(self, value):
        """Sends data to broker."""

    def pull(self) -> (str, Any):
        """Receives (topic, data) from broker.

        Should BLOCK the consumer!"""

    def list_topics(self, callback: Callable):
        """Lists all topics available in the broker."""

    def cancel(self):
        """Cancel subscription."""


class JSONQueue(Queue):
    """Queue implementation with JSON based serialization."""


class XMLQueue(Queue):
    """Queue implementation with XML based serialization."""


class PickleQueue(Queue):
    """Queue implementation with Pickle based serialization."""
