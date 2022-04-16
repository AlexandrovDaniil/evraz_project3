from datetime import datetime
from unittest.mock import Mock
import pytest
from attr import asdict
from book.application.services import Books
from book.application.errors import NotAvailable, NoBook, UserAlreadyHasBook, UserHasNotBook, WrongUser, WrongOper, \
    AnyNewBook
from pydantic import ValidationError


@pytest.fixture(scope='function')
def service_book(book_repo):
    return Books(book_repo=book_repo)


data_book = {
    "isbn13": 9781491954461,
    "tag": "mongo",
    "title": "MongoDB: The Definitive Guide, 3rd Edition",
    "subtitle": "Powerful and Scalable Data Storage",
    "authors": "Shannon Bradshaw, Kristina Chodorow",
    "pages": 514,
    "price": 29.0,
    "publisher": "O'Reilly Media",
    "desc": "Manage your data with a system",
    "year": 2019,
    "booking_time": None,
    "rating": 5,
    "isbn10": '12345678x',
    'language': 'English',
    "timestamp": datetime(2022, 4, 15, 20, 20, 20),
    'bought': False,

}

data_book2 = {
    "isbn13": 9781491954462,
    "tag": "mongo",
    "title": "wer",
    "subtitle": "Powerful and Scalable Data Storage",
    "authors": "Shannon Bradshaw, Kristina Chodorow",
    "pages": 514,
    "price": 29.0,
    "publisher": "O'Reilly Media",
    "desc": "Manage your data with a system",
    "year": 2020,
    "booking_time": None,
    "rating": 5,
    "isbn10": '12345678x',
    'language': 'English',
    "timestamp": datetime(2022, 4, 15, 20, 20, 20),
    'bought': False,

}

data_book3 = {
    "isbn13": 9781491954463,
    "tag": "mongo",
    "title": "ewq",
    "subtitle": "Powerful and Scalable Data Storage",
    "authors": "Shannon Bradshaw, Kristina Chodorow",
    "pages": 514,
    "price": 29.0,
    "publisher": "O'Reilly Media",
    "desc": "Manage your data with a system",
    "year": 2021,
    "booking_time": datetime(2024, 4, 15, 20, 20, 20),
    "rating": 5,
    "isbn10": '12345678x',
    'language': 'English',
    "timestamp": datetime(2022, 4, 15, 20, 20, 20),
    'bought': False,

}

data_book_history = {
    'book_id': 9781491954463,
    'user_id': 1,
    'action': 'take book',
    'booking_time': datetime(2022, 4, 15, 20, 20, 20),
    'id': 1
}

data_filter = {
    'authors': 'Shannon Bradshaw',
    'price': 'lt:50',
}


def test_parse_message(service_book):
    with pytest.raises(ValidationError):
        service_book.parse_message()


def test_send_to_user_any_books(service_book):
    service_book.book_repo.get_top_3.return_value = []
    with pytest.raises(AnyNewBook):
        service_book._send_top_to_user(tags=('mongo',), timestamp=datetime(2022, 4, 15, 20, 20, 20))


def test_send_to_user_wrong_args(service_book):
    with pytest.raises(ValidationError):
        service_book._send_top_to_user(timestamp=datetime(2022, 4, 15, 20, 20, 20))


def test_get_book(service_book):
    book = service_book.get_info(book_id=9781491954461)
    assert asdict(book) == data_book


def test_get_book_missing_id(service_book):
    with pytest.raises(ValidationError):
        service_book.get_info()


def test_get_wrong_book(service_book):
    service_book.book_repo.get_by_id.return_value = None
    with pytest.raises(NoBook):
        service_book.get_info(book_id=9781491954461)


def test_get_all(service_book):
    book = service_book.get_all()
    assert [asdict(book[0]), asdict(book[1])] == [data_book, data_book2]


def test_get_history(service_book):
    book_history = service_book.get_history(user_id=1)
    assert asdict(book_history[0]) == data_book_history


def test_get_history_missing_id(service_book):
    with pytest.raises(ValidationError):
        service_book.get_history()


def test_take_book_wrong_args(service_book):
    with pytest.raises(ValidationError):
        service_book.take_book(user_id=2)


def test_take_book_no_book(service_book):
    service_book.book_repo.get_by_id.return_value = None
    with pytest.raises(NoBook):
        service_book.take_book(user_id=2, book_id=9781491954461)


def test_take_book_user_already_has_book(service_book):
    wrong_data = service_book.book_repo.wrong_time_bought()
    service_book.book_repo.get_by_id.return_value = wrong_data
    with pytest.raises(UserAlreadyHasBook):
        service_book.take_book(user_id=2, book_id=1)


def test_take_book_not_available(service_book):
    wrong_data = service_book.book_repo.book_bought()
    service_book.book_repo.get_by_id.return_value = wrong_data
    with pytest.raises(NotAvailable):
        service_book.take_book(user_id=2, book_id=1)


def test_take_book(service_book):
    service_book.take_book(user_id=2, book_id=9781491954461)
    service_book.book_repo.add_books_history_row.assert_called_once()
    service_book.book_repo.update_booking_time.assert_called_once()


def test_return_book_missing_args(service_book):
    with pytest.raises(ValidationError):
        service_book.return_book()


def test_return_book_no_book(service_book):
    service_book.book_repo.get_by_id.return_value = None
    with pytest.raises(NoBook):
        service_book.return_book(user_id=2, book_id=9781491954461)


def test_return_book_user_has_not_book(service_book):
    service_book.book_repo.get_last_history_row.return_value = None
    with pytest.raises(UserHasNotBook):
        service_book.return_book(user_id=2, book_id=9781491954461)


def test_return_book_wrong_user(service_book):
    wrong_data = service_book.book_repo.wrong_time_bought()
    service_book.book_repo.get_by_id.return_value = wrong_data
    with pytest.raises(WrongUser):
        service_book.return_book(user_id=2, book_id=1)


def test_return_book(service_book):
    wrong_data = service_book.book_repo.wrong_time_bought()
    service_book.book_repo.get_by_id.return_value = wrong_data
    service_book.return_book(user_id=2, book_id=9781491954463)
    service_book.book_repo.update_booking_time.assert_called_once()


def test_buy_book_missing_args(service_book):
    with pytest.raises(ValidationError):
        service_book.buy_book()


def test_buy_book_no_book(service_book):
    service_book.book_repo.get_by_id.return_value = None
    with pytest.raises(NoBook):
        service_book.buy_book(user_id=2, book_id=9781491954461)


def test_buy_book_user_has_not_book(service_book):
    service_book.book_repo.get_last_history_row.return_value = None
    with pytest.raises(UserHasNotBook):
        service_book.buy_book(user_id=2, book_id=9781491954461)


def test_buy_book_wrong_user(service_book):
    wrong_data = service_book.book_repo.wrong_time_bought()
    service_book.book_repo.get_by_id.return_value = wrong_data
    with pytest.raises(WrongUser):
        service_book.buy_book(user_id=2, book_id=1)


def test_buy_book(service_book):
    wrong_data = service_book.book_repo.wrong_time_bought()
    service_book.book_repo.get_by_id.return_value = wrong_data
    service_book.buy_book(user_id=2, book_id=9781491954463)
    service_book.book_repo.buy_book.assert_called_once()


def test_active_book_missing_args(service_book):
    with pytest.raises(ValidationError):
        service_book.get_active_book()


def test_active_book_user_has_not_book(service_book):
    wrong_data = service_book.book_repo.book_bought()
    service_book.book_repo.get_by_id.return_value = wrong_data
    with pytest.raises(UserHasNotBook):
        service_book.get_active_book(user_id=2)


def test_active_book(service_book):
    booked_book = service_book.book_repo.wrong_time_bought()
    service_book.book_repo.get_by_id.return_value = booked_book
    book = service_book.get_active_book(user_id=2)
    assert asdict(book) == data_book3


def test_filter(service_book):
    book = service_book.search_by_filter(data_filter)
    assert asdict(book) == data_book


def test_filter_wrong_oper(service_book):
    data_filter['price'] = 'ddd:50'
    with pytest.raises(WrongOper):
        service_book.search_by_filter(data_filter)
