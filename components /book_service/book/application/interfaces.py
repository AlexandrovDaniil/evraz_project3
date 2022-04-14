from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Union

from .dataclasses import Book, BookHistory


class BooksRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[Book]: ...

    @abstractmethod
    def add_instance(self, book: Book): ...

    @abstractmethod
    def get_all(self) -> List[Book]: ...

    @abstractmethod
    def update_booking_time(self, book_id:int, booking_time: Optional[datetime]): ...

    @abstractmethod
    def delete_instance(self, id_: int): ...

    @abstractmethod
    def return_book(self, history_row: BookHistory): ...

    @abstractmethod
    def take_book(self, history_row: BookHistory): ...

    @abstractmethod
    def get_history(self, user_id: int) -> List[BookHistory]: ...

    @abstractmethod
    def buy_book(self, book_id: int): ...

    @abstractmethod
    def get_by_filter(self, authors: str, publisher: str, title: str) -> Optional[List[Book]]: ...

    @abstractmethod
    def get_by_filter_price(self, authors: str, publisher: str, title: str, oper: str, val: int) -> Optional[
        List[Book]]: ...
