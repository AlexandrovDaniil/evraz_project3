from book.application import services
from kombu import Connection

from evraz.classic.messaging_kombu import KombuConsumer

from .scheme import broker_scheme


def create_consumer(
    connection: Connection, book: services.Books
) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        book.parse_message,
        'ApiQueue',
    )

    return consumer
