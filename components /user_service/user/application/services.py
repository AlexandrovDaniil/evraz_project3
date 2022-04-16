from typing import Optional, List

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments
from classic.messaging import Message, Publisher

from . import errors, interfaces
from .dataclasses import User

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    name: str
    login: str
    password: str
    id: Optional[int]


@component
class Users:
    user_repo: interfaces.UsersRepo
    publisher: Optional[Publisher] = None

    @join_point
    @validate_arguments
    def get_info(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise errors.NoUser(id=user_id)
        return user

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        if not self.user_repo.get_by_login(user_info.login):
            new_user = user_info.create_obj(User)
            new_user = self.user_repo.add_instance(new_user)
            return new_user
        raise errors.LoginIsOccupied()

    @join_point
    @validate_arguments
    def login_user(self, user_login: str, user_password: str):
        user = self.user_repo.get_by_login(user_login)
        if not user:
            raise errors.NoUserLogin(login=user_login)
        if user.password == user_password:
            return user
        else:
            raise errors.WrongUserPassword()

    @join_point
    def get_all(self) -> List[User]:
        users = self.user_repo.get_all()
        return users

    def send_message(self, data: dict):
        all_users = self.get_all()
        if all_users:
            for user in all_users:
                print(f'Dear {user.name}, we have something to you!')
                print(f'Here is our new books compilation:')
                for tag in data:
                    print(f'For tag {tag}:')
                    for book in data[tag]:
                        print(f'\t{book["title"]}, rating: {book["rating"]}, publish year: {book["year"]}')
