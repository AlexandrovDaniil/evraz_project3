from datetime import datetime
from typing import List, Optional

from book.application import interfaces
from book.application.dataclasses import Book, BookHistory
from sqlalchemy import and_, asc, desc, or_

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):

    def get_by_id(self, book_id: int) -> Optional[Book]:
        query = self.session.query(Book).filter(Book.isbn13 == book_id)
        return query.first()

    def add_instance(self, book: Book):
        if not self.session.query(Book).filter(Book.isbn13 == book.isbn13
                                               ).one_or_none():
            self.session.add(book)
            self.session.flush()

    def get_all(self) -> List[Book]:
        query = self.session.query(Book).filter(Book.bought == False)
        return query.all()

    def update_booking_time(
        self, book_id: int, booking_time: Optional[datetime]
    ):
        self.session.query(Book).filter(Book.isbn13 == book_id).update(
            {Book.booking_time: booking_time}
        )
        self.session.flush()

    def get_history(self, user_id: int) -> List[BookHistory]:
        query = self.session.query(BookHistory).filter(
            BookHistory.user_id == user_id
        )
        return query.all()

    def get_last_history_row(self, user_id: int) -> BookHistory:
        query = self.session.query(BookHistory).filter(BookHistory.user_id == user_id). \
            order_by(desc(BookHistory.id)).first()
        return query

    def buy_book(self, book_id: int):
        self.session.query(Book).filter(Book.isbn13 == book_id
                                        ).update({Book.bought: True})
        self.session.flush()

    def add_books_history_row(self, history_row: BookHistory):
        self.session.add(history_row)
        self.session.flush()

    def get_by_filter(self, filter_data: dict) -> Optional[List[Book]]:
        query = self.session.query(Book).filter(Book.bought == False)
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
            query = query.filter(Book.authors.ilike(f'%{authors}%'))
        if 'publisher' in filter_data:
            publisher = filter_data['publisher']
            if isinstance(filter_data['publisher'], list):
                publisher = ','.join(publisher)
            query = query.filter(Book.publisher.ilike(f'%{publisher}%'))
        if 'keyword' in filter_data:
            keyword = filter_data['keyword']
            if isinstance(filter_data['keyword'], list):
                keyword = ','.join(keyword)
            query = query.filter(
                or_(
                    Book.title.ilike(f'%{keyword}%'),
                    Book.desc.ilike(f'%{keyword}%'),
                    Book.subtitle.ilike(f'%{keyword}%')
                )
            )
        return query

    @staticmethod
    def filter_price(filter_data: dict, query):
        if 'price' in filter_data:
            price = filter_data.pop('price')
            oper, val = price.split(':')
            if oper == 'lt':
                query = query.filter(Book.price < val)
            elif oper == 'gt':
                query = query.filter(Book.price > val)
            elif oper == 'lte':
                query = query.filter(Book.price <= val)
            elif oper == 'gte':
                query = query.filter(Book.price >= val)
            else:
                query = query.filter(Book.price == val)
        return query

    @staticmethod
    def sort_order_by(filter_data: dict, query):
        if 'order_by' in filter_data:
            if filter_data['order_by'] == 'price':
                query = query.order_by(desc(Book.price))
            elif filter_data['order_by'] == 'pages':
                query = query.order_by(desc(Book.pages))
        return query

    def get_top_3(self, tag: str, timestamp: datetime) -> Optional[List[Book]]:
        query = self.session.query(Book).filter(and_(Book.tag == tag, Book.timestamp == timestamp)). \
            order_by(desc(Book.rating), asc(Book.year)).limit(3)
        return query.all()
