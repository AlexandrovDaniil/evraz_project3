from typing import List, Optional

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
        query = BOOK.insert().values(
            author=book.author,
            published_year=book.published_year,
            title=book.title,
            user_id=None
        )
        self.session.execute(query)
        book = select(BOOK).order_by(desc(BOOK.c.id))
        book = self.session.execute(book).fetchone()
        return {'id_book': book.id, 'name': book.title}

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
