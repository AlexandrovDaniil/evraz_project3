from datetime import datetime
from unittest.mock import Mock
import pytest
from book.application import dataclasses, interfaces


@pytest.fixture(scope='function')
def book():
    return dataclasses.Book(

        isbn13=9781491954461,
        tag="mongo",
        title="MongoDB: The Definitive Guide, 3rd Edition",
        subtitle="Powerful and Scalable Data Storage",
        authors="Shannon Bradshaw, Kristina Chodorow",
        pages=514,
        price=29.0,
        publisher="O'Reilly Media",
        desc="Manage your data with a system",
        year=2019,
        booking_time=None,
        rating=5,
        isbn10='12345678x',
        language='English',
        timestamp=datetime(2022, 4, 15, 20, 20, 20),

    )


@pytest.fixture(scope='function')
def book2():
    return dataclasses.Book(

        isbn13=9781491954462,
        tag="mongo",
        title="wer",
        subtitle="Powerful and Scalable Data Storage",
        authors="Shannon Bradshaw, Kristina Chodorow",
        pages=514,
        price=29.0,
        publisher="O'Reilly Media",
        desc="Manage your data with a system",
        year=2020,
        booking_time=None,
        rating=5,
        isbn10='12345678x',
        language='English',
        timestamp=datetime(2022, 4, 15, 20, 20, 20)
    )


@pytest.fixture(scope='function')
def book3():
    return dataclasses.Book(

        isbn13=9781491954463,
        tag="mongo",
        title="ewq",
        subtitle="Powerful and Scalable Data Storage",
        authors="Shannon Bradshaw, Kristina Chodorow",
        pages=514,
        price=29.0,
        publisher="O'Reilly Media",
        desc="Manage your data with a system",
        year=2021,
        booking_time=None,
        rating=5,
        isbn10='12345678x',
        language='English',
        timestamp=datetime(2022, 4, 15, 20, 20, 20)
    )


@pytest.fixture(scope='function')
def wrong_time_bought():
    return dataclasses.Book(
        isbn13=9781491954463,
        tag="mongo",
        title="ewq",
        subtitle="Powerful and Scalable Data Storage",
        authors="Shannon Bradshaw, Kristina Chodorow",
        pages=514,
        price=29.0,
        publisher="O'Reilly Media",
        desc="Manage your data with a system",
        year=2021,
        booking_time=datetime(2024, 4, 15, 20, 20, 20),
        rating=5,
        isbn10='12345678x',
        language='English',
        timestamp=datetime(2022, 4, 15, 20, 20, 20),
        bought=False
    )



@pytest.fixture(scope='function')
def book_bought():
    return dataclasses.Book(
        isbn13=9781491954463,
        tag="mongo",
        title="ewq",
        subtitle="Powerful and Scalable Data Storage",
        authors="Shannon Bradshaw, Kristina Chodorow",
        pages=514,
        price=29.0,
        publisher="O'Reilly Media",
        desc="Manage your data with a system",
        year=2021,
        booking_time=None,
        rating=5,
        isbn10='12345678x',
        language='English',
        timestamp=datetime(2022, 4, 15, 20, 20, 20),
        bought=True
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
def book_repo(book, book2, book3, book_history, wrong_time_bought, book_bought):
    book_repo = Mock(interfaces.BooksRepo)
    book_repo.get_by_id = Mock(return_value=book)
    book_repo.wrong_time_bought = Mock(return_value=wrong_time_bought)
    book_repo.book_bought = Mock(return_value=book_bought)
    book_repo.add_instance = Mock()
    book_repo.get_all = Mock(return_value=[book, book2])
    book_repo.add_books_history_row = Mock()
    book_repo.update_booking_time = Mock()
    book_repo.get_history = Mock(return_value=[book_history])
    book_repo.get_last_history_row = Mock(return_value=book_history)
    book_repo.buy_book = Mock()
    book_repo.get_by_filter = Mock(return_value=book)
    book_repo.get_top_3 = Mock(return_value=[book, book2, book3])

    return book_repo
