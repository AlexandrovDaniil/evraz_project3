from book.application import dataclasses
from sqlalchemy.orm import registry, relationship

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.Book, tables.BOOK)

mapper.map_imperatively(dataclasses.BookHistory, tables.BOOK_HISTORY)

