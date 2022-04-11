from typing import Optional

import attr


@attr.dataclass
class Book:
    author: str
    published_year: int
    title: str
    id: Optional[int] = None
    user_id: Optional[int] = None
