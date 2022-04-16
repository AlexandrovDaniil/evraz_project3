from typing import Optional

import attr


@attr.dataclass
class User:
    name: str
    login: str
    password: str
    id: Optional[int] = None
