from typing import Optional

import attr


@attr.dataclass
class Book:
    title: str
    subtitle: str
    authors: str
    publisher: str
    isbn10: int
    isbn13: int
    pages: int
    year: int
    rating: int
    desc: str
    price: str
    language: str
    image: Optional[str] = None
    error: Optional[str] = None
    url: Optional[str] = None
    id: Optional[int] = None
    pdf: Optional[dict] = None
