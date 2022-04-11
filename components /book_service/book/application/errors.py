from classic.app.errors import AppError


class NoBook(AppError):
    msg_template = "No book with id '{id}'"
    code = 'books.no_book'

class NotAvailable(AppError):
    msg_template = "With id '{id}' not available"
    code = 'books.not_available'

class WrongUser(AppError):
    msg_template = "User with id '{user_id}' has not book with id '{book_id}'"
    code = 'books.wrong_user'