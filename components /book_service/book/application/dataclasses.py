from datetime import datetime
from typing import Optional

import attr


@attr.dataclass
class Book:
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
    bought: Optional[bool] = False
    booking_time: Optional[datetime] = None

    # image: Optional[str] = None
    # error: Optional[str] = None
    # url: Optional[str] = None
    # id: Optional[int] = None
    # pdf: Optional[dict] = None


@attr.dataclass
class BookHistory:
    book_id: int
    user_id: int
    action: str
    booking_time: datetime \
        # = attr.ib(factory=lambda: datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    id: Optional[int] = None
