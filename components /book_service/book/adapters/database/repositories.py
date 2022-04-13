from typing import List, Optional, Union

from sqlalchemy.orm import aliased

from book.application import interfaces
from book.application.dataclasses import Book
from .tables import BOOK
from classic.components import component
from classic.sql_storage import BaseRepository
from sqlalchemy import delete, select, insert, update, desc


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):

    def get_by_id(self, book_id: int) -> Optional[Book]:
        query = select(BOOK).where(BOOK.c.id == book_id)
        result = self.session.execute(query).fetchone()
        return result

    def add_instance(self, book: Book):
        self.session.add(book)
        self.session.flush()

    def get_all(self) -> List[Book]:
        query = select(BOOK)
        return self.session.execute(query).fetchall()

    def delete_instance(self, book_id: int):
        query = BOOK.delete().where(BOOK.c.id == book_id)
        return self.session.execute(query)

    def return_book(self, book_id: int):
        query = update(BOOK).where(BOOK.c.id == book_id).values(user_id=None)
        return self.session.execute(query)

    def take_book(self, book_id: int, user_id: int):
        query = update(BOOK).where(BOOK.c.id == book_id).values(user_id=user_id)
        return self.session.execute(query)

    def get_by_filter(self, authors: str, publisher: str, title: str) -> Optional[List[Book]]:
        result = self.session.query(BOOK).filter(BOOK.c.authors.like(f'%{authors}%')). \
            filter(BOOK.c.publisher.like(f'%{publisher}%')). \
            filter(BOOK.c.title.like(f'%{title}%')).all()
        return result

    def get_by_filter_price(self, authors: str, publisher: str, title: str, oper: str, val: int) -> Optional[List[Book]]:
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
