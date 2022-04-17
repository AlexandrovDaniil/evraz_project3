from datetime import datetime

import pytest
from book.adapters.database import tables
from book.adapters.database.repositories import BooksRepo
from book.application import dataclasses
from sqlalchemy.orm import registry


@pytest.fixture(scope='function')
def fill_db(session):
    books_data = [
        {
            'isbn13': 9781491954461,
            'tag': 'mongo',
            'title': 'MongoDB: The Definitive Guide, 3rd Edition',
            'subtitle': 'Powerful and Scalable Data Storage',
            'authors': 'Shannon Bradshaw, Kristina Chodorow',
            'pages': 514,
            'price': 29.0,
            'publisher': "O'Reilly Media",
            'desc': 'Manage your data with a system',
            'year': 2019,
            'booking_time': None,
            'rating': 5,
            'isbn10': '12345678x',
            'language': 'English',
            'timestamp': datetime(2022, 4, 15, 20, 20, 20),
            'bought': False,
        },
        {
            'isbn13': 9781491954462,
            'tag': 'mongo',
            'title': 'MongoDB: The Definitive Guide, 3rd Edition',
            'subtitle': 'Powerful and Scalable Data Storage',
            'authors': 'Shannon Bradshaw, Kristina Chodorow',
            'pages': 514,
            'price': 29.0,
            'publisher': "O'Reilly Media",
            'desc': 'Manage your data with a system',
            'year': 2020,
            'booking_time': None,
            'rating': 5,
            'isbn10': '12345678x',
            'language': 'English',
            'timestamp': datetime(2022, 4, 15, 20, 20, 20),
            'bought': False,
        },
    ]
    books_history_data = [
        {
            'book_id': 9781491954463,
            'user_id': 1,
            'booking_time': datetime(2022, 4, 15, 20, 20, 20),
            'id': 1
        }, {
            'book_id': 9781491954464,
            'user_id': 2,
            'booking_time': datetime(2021, 4, 15, 20, 20, 20),
            'id': 2
        }
    ]
    session.execute(tables.BOOK.insert(), books_data)
    session.execute(tables.BOOK_HISTORY.insert(), books_history_data)


@pytest.fixture(scope='function')
def mapping():
    mapper = registry()
    mapper.map_imperatively(dataclasses.Book, tables.BOOK)
    mapper.map_imperatively(dataclasses.BookHistory, tables.BOOK_HISTORY)


@pytest.fixture(scope='function')
def repo(transaction_context):
    return BooksRepo(context=transaction_context)


book_data_new = {
    'isbn13': 9781491954463,
    'tag': 'mongo',
    'title': 'MongoDB: The Definitive Guide, 3rd Edition',
    'subtitle': 'Powerful and Scalable Data Storage',
    'authors': 'Shannon Bradshaw, Kristina Chodorow',
    'pages': 514,
    'price': 29.0,
    'publisher': "O'Reilly Media",
    'desc': 'Manage your data with a system',
    'year': 2019,
    'booking_time': None,
    'rating': 5,
    'isbn10': '12345678x',
    'language': 'English',
    'timestamp': datetime(2022, 4, 15, 20, 20, 20),
    'bought': False,
}

book_history_data_new = {
    'book_id': 9781491954465,
    'user_id': 1,
    'booking_time': datetime(2032, 4, 15, 20, 20, 20),
    'id': 3
}


def test__get_by_id(repo, fill_db):
    result = repo.get_by_id(book_id=9781491954462)
    assert result.isbn13 == 9781491954462


def test__add_instance(repo, fill_db):
    book = dataclasses.Book(**book_data_new)
    repo.add_instance(book)
    result = repo.get_by_id(9781491954463)
    assert result.isbn13 == 9781491954463


def test__get_all(repo, fill_db):
    result = repo.get_all()
    assert len(result) == 2


def test__update_booking_time(repo, fill_db):
    repo.update_booking_time(9781491954462, datetime(2032, 4, 15, 20, 20, 20))
    result = repo.get_by_id(9781491954462)
    assert result.booking_time == datetime(2032, 4, 15, 20, 20, 20)


def test__get_history(repo, fill_db):
    result = repo.get_history(user_id=1)
    assert result[0].book_id == 9781491954463


def test__get_last_history_row(repo, fill_db):
    result = repo.get_last_history_row(user_id=1)
    assert result.book_id == 9781491954463


def test__buy_book(repo, fill_db):
    repo.buy_book(book_id=9781491954461)
    result = repo.get_by_id(book_id=9781491954461)
    assert result.bought is True


def test__add_books_history_row(repo, fill_db):
    book_history_row = dataclasses.BookHistory(**book_history_data_new)
    repo.add_books_history_row(book_history_row)
    result = repo.get_last_history_row(user_id=1)
    assert result.book_id == 9781491954465


def test__get_top_3(repo, fill_db):
    result = repo.get_top_3(
        tag='mongo', timestamp=datetime(2022, 4, 15, 20, 20, 20)
    )
    assert result[0].isbn13 == 9781491954461


def test__get_by_filter(repo, fill_db):
    result = repo.get_by_filter({'keyword': 'MongoDB: The Definitive'})
    assert result[0].isbn13 == 9781491954461
