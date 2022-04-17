from kombu import Connection

from classic.messaging_kombu import KombuConsumer

from user.application import services

from .scheme import broker_scheme


def create_consumer(
    connection: Connection, sender: services.MailSender
) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        sender.send_message_to_users,
        'Top3ApiQueue',
    )

    return consumer
