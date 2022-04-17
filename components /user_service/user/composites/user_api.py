from user.adapters import user_api, database, message_bus, mail_sending
from user.application import services
from classic.sql_storage import TransactionContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kombu import Connection



class Settings:
    db = database.Settings()
    user_api = user_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)
    Session = sessionmaker(bind=engine)
    users_repo = database.repositories.UsersRepo(context=context)


class MailSending:
    sender = mail_sending.MailSender()


class Application:
    is_dev_mode = Settings.user_api.IS_DEV_MODE
    users = services.Users(user_repo=DB.users_repo)
    sender = services.MailSender(
        user_repo=DB.users_repo,
        mail_sender=MailSending.sender,
    )


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    consumer = message_bus.create_consumer(connection, Application.sender)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBus.connection)


class Aspects:
    services.join_points.join(DB.context)
    user_api.join_points.join(DB.context)


app = user_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    users=Application.users,

)
