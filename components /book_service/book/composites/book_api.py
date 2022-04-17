from book.adapters import book_api, database, message_bus
from book.application import services
from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Settings:
    db = database.Settings()
    book_api = book_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)
    Session = sessionmaker(bind=engine)
    books_repo = database.repositories.BooksRepo(context=context)


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class Application:
    is_dev_mode = Settings.book_api.IS_DEV_MODE
    books = services.Books(
        book_repo=DB.books_repo, publisher=MessageBus.publisher
    )


class MessageBusCons:
    connection = Connection(Settings.message_bus.BROKER_URL)
    consumer = message_bus.create_consumer(connection, Application.books)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBusCons.connection)


class Aspects:
    services.join_points.join(DB.context)
    book_api.join_points.join(MessageBus.publisher, DB.context)


app = book_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    books=Application.books,
)
