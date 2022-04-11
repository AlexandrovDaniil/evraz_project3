from kombu import Exchange, Queue

from classic.messaging_kombu import BrokerScheme

broker_scheme = BrokerScheme(
    Queue('TestApiQueue', Exchange('TestApiExchange'), max_length=100)
)
