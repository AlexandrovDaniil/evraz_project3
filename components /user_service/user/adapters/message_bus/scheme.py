from evraz.classic.messaging_kombu import BrokerScheme
from kombu import Exchange, Queue

broker_scheme = BrokerScheme(Queue('Top3ApiQueue', Exchange('Top3ApiExchange')))
