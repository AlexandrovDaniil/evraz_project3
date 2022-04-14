from datetime import datetime
from typing import List, Optional, Union

from sqlalchemy.orm import aliased

from book.application import interfaces
from book.application.dataclasses import Book, BookHistory
from .tables import BOOK, BOOK_HISTORY
from classic.components import component
from classic.sql_storage import BaseRepository
from sqlalchemy import delete, select, insert, update, desc, or_


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):

    def get_by_id(self, book_id: int) -> Optional[Book]:
        query = select(BOOK).where(BOOK.c.isbn13 == book_id)
        result = self.session.execute(query).fetchone()
        return result

    def add_instance(self, book: Book):
        self.session.add(book)
        self.session.flush()

    def get_all(self) -> List[Book]:
        query = select(BOOK).where(BOOK.c.bought == False)
        return self.session.execute(query).fetchall()

    def delete_instance(self, book_id: int):
        query = BOOK.delete().where(BOOK.c.id == book_id)
        return self.session.execute(query)

    def update_booking_time(self, book_id: int, booking_time: Optional[datetime]):
        query = update(BOOK).where(BOOK.c.isbn13 == book_id).values(booking_time=booking_time)
        return self.session.execute(query)

    def get_history(self, user_id: int) -> List[BookHistory]:
        query = select(BOOK_HISTORY).where(BOOK_HISTORY.c.user_id == user_id)
        return self.session.execute(query).fetchall()

    def buy_book(self, book_id: int):
        query = update(BOOK).where(BOOK.c.isbn13 == book_id).values(bought=True)
        return self.session.execute(query)

    def return_book(self, history_row: BookHistory):
        self.session.add(history_row)
        self.session.flush()
        # query = update(BOOK).where(BOOK.c.id == book_id).values(user_id=None)
        # return self.session.execute(query)

    def take_book(self, history_row: BookHistory):
        # query = update(BOOK).where(BOOK.c.id == book_id).values(user_id=user_id)
        # return self.session.execute(query)
        self.session.add(history_row)
        self.session.flush()

    # def get_by_filter(self, authors: str, publisher: str, title: str) -> Optional[List[Book]]:
    def get_by_filter(self, filter_data: dict) -> Optional[List[Book]]:
        # result = self.session.query(BOOK).filter(BOOK.c.authors.like(f'%{authors}%')). \
        #     filter(BOOK.c.publisher.like(f'%{publisher}%')). \
        #     filter(BOOK.c.title.like(f'%{title}%')).all()
        # return result
        query = self.session.query(BOOK)
        query = self.default_filters(filter_data, query)
        query = self.filter_price(filter_data, query)
        query = self.sort_order_by(filter_data, query)
        return query.all()

    @staticmethod
    def default_filters(filter_data: dict, query):
        if 'authors' in filter_data:
            authors = filter_data['authors']
            if isinstance(filter_data['authors'], list):
                authors = ','.join(authors)
            query = query.filter(BOOK.c.authors.ilike(f'%{authors}%'))
        if 'publisher' in filter_data:
            publisher = filter_data['publisher']
            query = query.filter(BOOK.c.publisher.ilike(f'%{publisher}%'))
        if 'keyword' in filter_data:
            keyword = filter_data['keyword']
            query = query.filter(or_(BOOK.c.title.ilike(f'%{keyword}%'),
                                     BOOK.c.desc.ilike(f'%{keyword}%'),
                                     BOOK.c.subtitle.ilike(f'%{keyword}%')))
        return query

    @staticmethod
    def filter_price(filter_data: dict, query):
        if 'price' in filter_data:
            price = filter_data.pop('price')
            oper, val = price.split(':')
            if oper == 'lt':
                query = query.filter(BOOK.c.price < val)
            elif oper == 'gt':
                query = query.filter(BOOK.c.price > val)
            elif oper == 'lte':
                query = query.filter(BOOK.c.price <= val)
            elif oper == 'gte':
                query = query.filter(BOOK.c.price >= val)
            else:
                query = query.filter(BOOK.c.price == val)
        return query

    @staticmethod
    def sort_order_by(filter_data: dict, query):
        if 'order_by' in filter_data:
            if filter_data['order_by'] == 'price':
                query = query.order_by(BOOK.c.price.desc())
            elif filter_data['order_by'] == 'pages':
                query = query.order_by(BOOK.c.pages.desc())
        return query
