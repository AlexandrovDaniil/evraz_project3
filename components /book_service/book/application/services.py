import threading
from datetime import datetime, timedelta
from typing import Optional, List, Union

import requests
import attr
from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments
from classic.messaging import Message, Publisher

from . import errors, interfaces
from .dataclasses import Book, BookHistory

join_points = PointCut()
join_point = join_points.join_point


class BookInfo(DTO):
    title: str
    subtitle: str
    authors: str
    publisher: str
    isbn10: str
    isbn13: int
    pages: int
    year: int
    rating: int
    desc: str
    price: int
    language: str
    tag: str
    timestamp: datetime
    bought: Optional[bool] = False
    booking_time: Optional[datetime] = None


class BookHistoryInfo(DTO):
    book_id: int
    user_id: int
    action: str
    booking_time: datetime
    id: Optional[int] = None


@component
class Books:
    book_repo: interfaces.BooksRepo
    publisher: Optional[Publisher] = None

    def _is_user_has_book(self, user_id: int) -> bool:
        history = self.get_history(user_id)
        if history:
            last_row = history[-1]
            last_book = self.book_repo.get_by_id(last_row.book_id)
            if last_book.booking_time is None or last_book.booking_time < datetime.utcnow() or last_book.bought:
                return False
            return True
        return False

    def _send_top_to_user(self, tags: tuple, timestamp: datetime):
        top_books_by_tag = {}
        for tag in tags:
            res = []
            top_books = self.book_repo.get_top_3(tag, timestamp)
            for book in top_books:
                prep_d = {'title': book.title,
                          'rating': book.rating,
                          'year': book.year}
                res.append(prep_d)
            top_books_by_tag[tag] = res
        self.publisher.publish(Message('Top3ApiExchange', {'data': top_books_by_tag}))

    @join_point
    @validate_arguments
    def get_info(self, book_id: int):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise errors.NoBook(id=book_id)
        return book

    @join_point
    @validate_arguments
    def add_book(self, tags: tuple):
        books_ids = {}
        threads = []
        timestamp = datetime.utcnow()
        for tag in tags:
            books_ids[tag] = []
            r = requests.get(f'https://api.itbook.store/1.0/search/{tag}').json()
            page_count = (int(r['total']) // 10) + (1 if int(r['total']) % 10 != 0 else 0)
            page_count = page_count if page_count < 5 else 5
            for i in range(1, page_count + 1):
                t = threading.Thread(target=self.thread_add, kwargs={'tag': tag, 'page': i, 'timestamp': timestamp})
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()
        self._send_top_to_user(tags, timestamp)

    @join_point
    @validate_arguments
    def thread_add(self, tag: str, page: int, timestamp: datetime):
        books_ids = []
        book_page = requests.get(f'https://api.itbook.store/1.0/search/{tag}/{page}').json()
        for book in book_page['books']:
            books_ids.append(book['isbn13'])
        for book_id in books_ids:
            book = requests.get(f'https://api.itbook.store/1.0/books/{int(book_id)}').json()
            book['price'] = float(book['price'][1:])
            book_info = BookInfo(
                title=book['title'],
                subtitle=book['subtitle'],
                authors=book['authors'],
                publisher=book['publisher'],
                isbn10=book['isbn10'],
                isbn13=book['isbn13'],
                pages=book['pages'],
                year=book['year'],
                rating=book['rating'],
                desc=book['desc'],
                price=book['price'],
                language=book['language'],
                tag=tag,
                timestamp=timestamp
            )
            new_book = book_info.create_obj(Book)
            self.book_repo.add_instance(new_book)
            # new_books[tag].append(book)

            # new_books[tag] = sorted(new_books[tag], key=lambda x: (x['rating'], -int(x['year'])), reverse=True)[:3]
        # self._send_top_to_user(new_books)

    @join_point
    @validate_arguments
    def search_by_filter(self, filter_data: dict):
        if 'price' in filter_data:
            price = filter_data['price']
            oper, val = price.split(':')
            if oper not in ('lt, gt, lte, gte, eq') or not isinstance(val, (int, float)):
                raise errors.WrongOperOrValue()
        res = self.book_repo.get_by_filter(filter_data)
        return res

    @join_point
    def get_all(self) -> List[Book]:
        books = self.book_repo.get_all()
        return books

    @join_point
    def get_history(self, user_id: int) -> List[BookHistory]:
        history_rows = self.book_repo.get_history(user_id)
        return history_rows

    @join_point
    @validate_arguments
    def return_book(self, book_id: int, user_id: int):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise errors.NoBook(id=book_id)
        if self._is_user_has_book(user_id):
            active_book = self.get_active_book(user_id)
            if active_book.isbn13 == book_id:
                self.book_repo.update_booking_time(book_id, None)
            else:
                raise errors.WrongUser(id=book_id)
        else:
            raise errors.UserHasNotBook()

    @join_point
    @validate_arguments
    def take_book(self, book_id: int, user_id: int, period: int = 7):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise errors.NoBook(id=book_id)
        if not self._is_user_has_book(user_id):
            if book.booking_time is None or book.booking_time < datetime.utcnow() and book.bought is False:
                time_of_book = datetime.utcnow() + timedelta(minutes=period)
                book_history = BookHistoryInfo(
                    book_id=book_id,
                    user_id=user_id,
                    action='take book',
                    booking_time=time_of_book
                )
                new_row_history = book_history.create_obj(BookHistory)
                self.book_repo.take_book(new_row_history)
                self.book_repo.update_booking_time(book_id, time_of_book)

            else:
                raise errors.NotAvailable(id=book_id)
        else:
            raise errors.UserAlreadyHasBook(id=user_id)

    @join_point
    @validate_arguments
    def buy_book(self, user_id: int, book_id: int):
        last_book = self.get_history(user_id)[-1]
        book = self.book_repo.get_by_id(last_book.book_id)
        if not book:
            raise errors.NoBook(id=book_id)
        if self._is_user_has_book(user_id):
            active_book = self.get_active_book(user_id)
            if active_book.isbn13 == book_id:
                self.book_repo.buy_book(book_id)
            else:
                raise errors.WrongUser(book_id=book_id)
        else:
            raise errors.UserHasNotBook()

    @join_point
    @validate_arguments
    def get_active_book(self, user_id: int) -> Union[Book, str]:
        last_book = self.get_history(user_id)[-1]
        book = self.book_repo.get_by_id(last_book.book_id)
        if book.booking_time is None or book.booking_time < datetime.utcnow() or book.bought:
            return 'User has not active book'
        else:
            return book
