from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import User


class UsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[User]: ...

    @abstractmethod
    def add_instance(self, user: User): ...

    @abstractmethod
    def get_all(self) -> List[User]: ...

    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]: ...


class MailSender(ABC):

    @abstractmethod
    def send(self, users: List[User], data: dict):
        ...
