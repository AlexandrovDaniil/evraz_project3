from typing import List, Optional

from user.application import interfaces
from user.application.dataclasses import User
from classic.components import component
from classic.sql_storage import BaseRepository


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def get_by_id(self, user_id: int) -> Optional[User]:
        query = self.session.query(User).filter(User.id == user_id)
        return query.first()

    def add_instance(self, user: User):
        self.session.add(user)
        self.session.flush()
        return user

    def get_all(self) -> List[User]:
        query = self.session.query(User)
        return query.all()

    def get_by_login(self, user_login: str) -> Optional[User]:
        query = self.session.query(User).filter(User.login == user_login)
        return query.first()
