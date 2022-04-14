from kombu import Exchange, Queue

from classic.messaging_kombu import BrokerScheme

broker_scheme = BrokerScheme(
    Queue('TestApiQueue', Exchange('TestApiExchange')),
    Queue('Top3ApiQueue', Exchange('Top3ApiExchange'))
)
