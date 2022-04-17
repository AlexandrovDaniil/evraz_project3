from evraz.classic.app.errors import AppError


class NoBook(AppError):
    msg_template = "No book with id '{id}'"
    code = 'books.no_book'


class WrongBook(AppError):
    msg_template = 'Wrong book'
    code = 'books.wrong_book'


class WrongOper(AppError):
    msg_template = 'This filter operator is not available'
    code = 'books.no_oper'


class UserAlreadyHasBook(AppError):
    msg_template = 'This user already has book'
    code = 'books.user_has_book'


class UserHasNotBook(AppError):
    msg_template = 'This user has not active book'
    code = 'books.user_has_not_book'


class NotAvailable(AppError):
    msg_template = "With id '{id}' not available"
    code = 'books.not_available'


class WrongUser(AppError):
    msg_template = "User has not book with id '{book_id}'"
    code = 'books.wrong_user'


class AnyNewBook(AppError):
    msg_template = 'CLI command did not add any new books'
    code = 'user.any_new_book'
