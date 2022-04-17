from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from .dataclasses import Book, BookHistory


class BooksRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[Book]:
        ...

    @abstractmethod
    def add_instance(self, book: Book):
        ...

    @abstractmethod
    def get_all(self) -> List[Book]:
        ...

    @abstractmethod
    def update_booking_time(
        self, book_id: int, booking_time: Optional[datetime]
    ):
        ...

    @abstractmethod
    def add_books_history_row(self, history_row: BookHistory):
        ...

    @abstractmethod
    def get_history(self, user_id: int) -> List[BookHistory]:
        ...

    @abstractmethod
    def get_last_history_row(self, user_id: int) -> BookHistory:
        ...

    @abstractmethod
    def buy_book(self, book_id: int):
        ...

    @abstractmethod
    def get_by_filter(self, filter_data: dict) -> Optional[List[Book]]:
        ...

    @abstractmethod
    def get_top_3(self, tag: str, timestamp: datetime) -> Optional[List[Book]]:
        ...
