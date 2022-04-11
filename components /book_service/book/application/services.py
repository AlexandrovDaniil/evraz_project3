from typing import Optional, List

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments
from classic.messaging import Message, Publisher

from . import errors, interfaces
from .dataclasses import Book

join_points = PointCut()
join_point = join_points.join_point


class BookInfo(DTO):
    author: str
    published_year: int
    title: str
    id: Optional[int]
    user_id: Optional[int]


@component
class Books:
    book_repo: interfaces.BooksRepo
    publisher: Optional[Publisher] = None

    @join_point
    @validate_arguments
    def get_info(self, id: int):
        book = self.book_repo.get_by_id(id)
        if not book:
            raise errors.NoBook(id=id)
        return book

    @join_point
    @validate_with_dto
    def add_book(self, book_info: BookInfo):
        new_book = book_info.create_obj(Book)
        new_book = self.book_repo.add_instance(new_book)
        if self.publisher:
            self.publisher.plan(
                Message('ApiExchange',
                        {'obj_type': 'book',
                         'action': 'create',
                         'data': new_book})
            )

    @join_point
    @validate_arguments
    def delete_book(self, id: int):
        book = self.book_repo.get_by_id(id)
        if not book:
            raise errors.NoBook(id=id)
        self.book_repo.delete_instance(id)
        if self.publisher:
            self.publisher.plan(
                Message('ApiExchange',
                        {'obj_type': 'book',
                         'action': 'delete',
                         'data': {'id_book': id}})
            )

    @join_point
    def get_all(self) -> List[Book]:
        books = self.book_repo.get_all()
        return books

    @join_point
    @validate_arguments
    def return_book(self, book_id: int, user_id: int):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise errors.NoBook(id=book_id)
        if book.user_id == user_id:
            self.book_repo.return_book(book_id)
            if self.publisher:
                self.publisher.plan(
                    Message('ApiExchange',
                            {'obj_type': 'user_book',
                             'action': 'return',
                             'data': {'id_book': book_id,
                                      'id_user': user_id,
                                      'book_title': book.title}

                             })
                )
        else:
            raise errors.WrongUser(book_id=book_id, user_id=user_id)

    @join_point
    @validate_arguments
    def take_book(self, book_id: int, user_id: int):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise errors.NoBook(id=book_id)
        if book.user_id is None:
            self.book_repo.take_book(book_id=book_id, user_id=user_id)
            if self.publisher:
                self.publisher.plan(
                    Message('ApiExchange',
                            {'obj_type': 'user_book',
                             'action': 'take',
                             'data': {'id_book': book_id,
                                      'id_user': user_id,
                                      'book_title': book.title}
                             })
                )
        else:
            raise errors.NotAvailable(id=book_id)
