from kombu import Connection

from classic.messaging_kombu import KombuConsumer

from book.application import services

from .scheme import broker_scheme


def create_consumer(
    connection: Connection, book: services.Books
) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        book.add_book,
        'TestApiQueue',
    )

    return consumer
