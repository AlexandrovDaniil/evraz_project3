from datetime import datetime
from typing import List, Optional, Union

from sqlalchemy.orm import aliased

from book.application import interfaces
from book.application.dataclasses import Book, BookHistory
from .tables import BOOK, BOOK_HISTORY
from classic.components import component
from classic.sql_storage import BaseRepository
from sqlalchemy import delete, select, insert, update, desc


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

    def get_by_filter(self, authors: str, publisher: str, title: str) -> Optional[List[Book]]:
        result = self.session.query(BOOK).filter(BOOK.c.authors.like(f'%{authors}%')). \
            filter(BOOK.c.publisher.like(f'%{publisher}%')). \
            filter(BOOK.c.title.like(f'%{title}%')).all()
        return result

    def get_by_filter_price(self, authors: str, publisher: str, title: str, oper: str, val: int) -> Optional[
        List[Book]]:
        if oper == 'lt':
            result = self.session.query(BOOK).filter(BOOK.c.authors.like(f'%{authors}%')). \
                filter(BOOK.c.publisher.like(f'%{publisher}%')). \
                filter(BOOK.c.title.like(f'%{title}%')). \
                filter(BOOK.c.price < val).all()
            return result
        elif oper == 'gt':
            result = self.session.query(BOOK).filter(BOOK.c.authors.like(f'%{authors}%')). \
                filter(BOOK.c.publisher.like(f'%{publisher}%')). \
                filter(BOOK.c.title.like(f'%{title}%')). \
                filter(BOOK.c.price > val).all()
            return result
        elif oper == 'lte':
            result = self.session.query(BOOK).filter(BOOK.c.authors.like(f'%{authors}%')). \
                filter(BOOK.c.publisher.like(f'%{publisher}%')). \
                filter(BOOK.c.title.like(f'%{title}%')). \
                filter(BOOK.c.price <= val).all()
            return result
        elif oper == 'gte':
            result = self.session.query(BOOK).filter(BOOK.c.authors.like(f'%{authors}%')). \
                filter(BOOK.c.publisher.like(f'%{publisher}%')). \
                filter(BOOK.c.title.like(f'%{title}%')). \
                filter(BOOK.c.price >= val).all()
            return result
        else:
            result = self.session.query(BOOK).filter(BOOK.c.authors.like(f'%{authors}%')). \
                filter(BOOK.c.publisher.like(f'%{publisher}%')). \
                filter(BOOK.c.title.like(f'%{title}%')). \
                filter(BOOK.c.price == val).all()
            return result
