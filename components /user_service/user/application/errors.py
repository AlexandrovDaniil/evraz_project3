from classic.app.errors import AppError


class NoUser(AppError):
    msg_template = "No user with id '{id}'"
    code = 'user.no_user'


class NoUserLogin(AppError):
    msg_template = "No user with login '{login}'"
    code = 'user.no_user_login'


class LoginIsOccupied(AppError):
    msg_template = 'This login is already occupied'
    code = 'user.login_is_occupied'


class WrongUserPassword(AppError):
    msg_template = 'Wrong password'
    code = 'user.wrong_password'
