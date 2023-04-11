from src.broker import Broker
from unittest.mock import MagicMock, patch
from src.broker import Serializer

broker = Broker()

fake_subscriber1 = MagicMock()
fake_subscriber2 = MagicMock()

broker.subscribe("/t1", fake_subscriber1, Serializer.JSON)
broker.subscribe("/t2", fake_subscriber1, Serializer.JSON)
broker.subscribe("/t2", fake_subscriber2, Serializer.PICKLE)

print(broker.list_subscriptions("/t1"))