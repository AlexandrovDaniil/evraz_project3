from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import Book


class BooksRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[Book]: ...

    @abstractmethod
    def add_instance(self, book: Book): ...

    @abstractmethod
    def get_all(self) -> List[Book]: ...

    @abstractmethod
    def delete_instance(self, id_: int): ...

    @abstractmethod
    def return_book(self, book_id: int): ...

    @abstractmethod
    def take_book(self, book_id: int, user_id: int): ...
