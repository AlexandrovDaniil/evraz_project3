from classic.http_api import App
from classic.http_auth import Authenticator
from user.application import services

from . import auth, controllers


def create_app(
    is_dev_mode: bool,
    users: services.Users,
) -> App:
    app = App(prefix='/api')
    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)
    if is_dev_mode:
        authenticator.set_strategies(auth.jwt_strategy)

    app.register(controllers.Users(authenticator=authenticator, users=users))
    return app
