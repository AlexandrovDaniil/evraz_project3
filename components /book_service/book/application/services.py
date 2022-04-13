from typing import Optional, List

import requests
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
    # image: Optional[str]
    # url: Optional[str]
    id: Optional[int] = None
    # pdf: Optional[dict] = None
    # error: Optional[str] = None


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
    @validate_arguments
    def add_book(self, tags: tuple):
        books_ids = []
        new_book_list = []
        for tag in tags:
            r = requests.get(f'https://api.itbook.store/1.0/search/{tag}').json()
            page_count = (int(r['total']) // 10) + (1 if int(r['total']) % 10 != 0 else 0)
            page_count = page_count if page_count < 5 else 5
            for i in range(1, page_count + 1):
                book_page = requests.get(f'https://api.itbook.store/1.0/search/{tag}/{i}').json()
                for book in book_page['books']:
                    books_ids.append(book['isbn13'])
        for book_id in books_ids:
            book = requests.get(f'https://api.itbook.store/1.0/books/{book_id}').json()
            new_book_list.append(book)
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
                language=book['language']
            )
            book = book_info.create_obj(Book)
            self.book_repo.add_instance(book)

        top_list = sorted(new_book_list, key=lambda x: (x['rating'], -int(x['year'])), reverse=True)[:3]
        for i in top_list:
            print(i['title'], i['rating'], i['year'])

    @join_point
    @validate_arguments
    def search_by_filter(self, filter_data: dict):
        if 'order_by' in filter_data:
            order_by = filter_data.pop('order_by')
        else:
            order_by = None
        if 'authors' not in filter_data:
            filter_data['authors'] = '%'
        if 'publisher' not in filter_data:
            filter_data['publisher'] = '%'
        if 'title' not in filter_data:
            filter_data['title'] = '%'

        if 'price' not in filter_data:
            res = self.book_repo.get_by_filter(**filter_data)

        else:
            price = filter_data.pop('price')
            oper, val = price.split(':')
            if oper not in ('lt, gt, lte, gte, eq'):
                raise errors.WrongOper(oper=oper)
            val = int(val)
            res = self.book_repo.get_by_filter_price(filter_data['authors'], filter_data['publisher'],
                                                     filter_data['title'], oper, val)

        if order_by == 'price':
            return sorted(res, key=lambda x: (x['price']), reverse=True)
        elif order_by == 'pages':
            return sorted(res, key=lambda x: (x['pages']), reverse=True)

        return res

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
