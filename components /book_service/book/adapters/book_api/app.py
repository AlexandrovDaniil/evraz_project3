from book.application import services
from classic.http_api import App
from classic.http_auth import Authenticator

from . import auth, controllers


def create_app(
        is_dev_mode: bool,
        books: services.Books,
) -> App:
    app = App(prefix='/api')
    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)
    if is_dev_mode:
        authenticator.set_strategies(auth.jwt_strategy)
    app.register(controllers.Books(authenticator=authenticator, books=books))
    return app
