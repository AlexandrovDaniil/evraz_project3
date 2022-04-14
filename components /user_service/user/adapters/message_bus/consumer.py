from kombu import Connection

from classic.messaging_kombu import KombuConsumer

from user.application import services

from .scheme import broker_scheme


def create_consumer(
    connection: Connection, user: services.Users
) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        user.send_message,
        'Top3ApiQueue',
    )

    return consumer
