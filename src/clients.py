"""Prototype broker clients: consumer + producer."""
from src.log import get_logger
from src.middleware import PickleQueue, MiddlewareType


class Consumer:
    """Consumer implementation"""

    def __init__(self, topic, queue_type=PickleQueue):
        """Initialize Queue"""
        self.topic = topic
        self.queue = queue_type(f"{topic}", _type=MiddlewareType.CONSUMER)
        self.logger = get_logger(f"Consumer {topic}")
        self.received = []

    def run(self, events=10):
        """Consume at most <events> events."""
        for _ in range(events):
            topic, data = self.queue.pull()
            self.logger.info("%s: %s", topic, data)
            self.received.append(data)


class Producer:
    """Producer implementation"""

    def __init__(self, topic, value_generator, queue_type=PickleQueue):
        """Initialize Queue."""
        self.logger = get_logger(f"Producer {topic}")

        if isinstance(topic, list):
            self.queue = [
                queue_type(subtopic, _type=MiddlewareType.PRODUCER)
                for subtopic in topic
            ]
        else:
            self.queue = [queue_type(topic, _type=MiddlewareType.PRODUCER)]
        self.produced = []
        self.gen = value_generator

    def run(self, events=10):
        """Produce at most <events> events."""
        for _ in range(events):
            for queue, value in zip(self.queue, self.gen()):
                queue.push(value)
                self.logger.info("%s: %s", queue.topic, value)

                self.produced.append(value)
