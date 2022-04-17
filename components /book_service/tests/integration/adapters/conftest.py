from datetime import datetime
from unittest.mock import Mock

import pytest
from book.adapters import book_api
from book.application import dataclasses, services
from falcon import testing


@pytest.fixture(scope='function')
def book():
    return dataclasses.Book(
        isbn13=9781491954461,
        tag='mongo',
        title='MongoDB: The Definitive Guide, 3rd Edition',
        subtitle='Powerful and Scalable Data Storage',
        authors='Shannon Bradshaw, Kristina Chodorow',
        pages=514,
        price=29.0,
        publisher="O'Reilly Media",
        desc='Manage your data with a system',
        year=2019,
        booking_time=None,
        rating=5,
        isbn10='12345678x',
        language='English',
        timestamp=datetime(2022, 4, 15, 20, 20, 20),
    )


@pytest.fixture(scope='function')
def book_history():
    return dataclasses.BookHistory(
        book_id=9781491954463,
        user_id=1,
        booking_time=datetime(2022, 4, 15, 20, 20, 20),
        id=1
    )


@pytest.fixture(scope='function')
def books_service(book, book_history):
    service = Mock(services.Books)
    service.get_info = Mock(return_value=book)
    service.get_all = Mock(return_value=[book])
    service.search_by_filter = Mock(return_value=[book])
    service.take_book = Mock()
    service.return_book = Mock()
    service.buy_book = Mock()
    service.get_history = Mock(return_value=[book_history])
    service.get_active_book = Mock(return_value=book)
    return service


@pytest.fixture(scope='function')
def client(books_service):
    app = book_api.create_app(is_dev_mode=True, books=books_service)

    return testing.TestClient(app)
