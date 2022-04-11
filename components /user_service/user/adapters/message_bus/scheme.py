from kombu import Exchange, Queue

from classic.messaging_kombu import BrokerScheme

broker_scheme = BrokerScheme(
    Queue('ApiQueue', Exchange('ApiExchange'), max_length=100)
)
