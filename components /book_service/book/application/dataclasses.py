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
    price: float
    language: str
    tag: str
    timestamp: datetime
    bought: Optional[bool] = False
    booking_time: Optional[datetime] = None


@attr.dataclass
class BookHistory:
    book_id: int
    user_id: int
    action: str
    booking_time: datetime
    id: Optional[int] = None
