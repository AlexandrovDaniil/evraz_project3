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
    user_name: str
    login: str
    password: str
    id: Optional[int]


@component
class Users:
    user_repo: interfaces.UsersRepo
    publisher: Optional[Publisher] = None

    @join_point
    @validate_arguments
    def get_info(self, id: int):
        user = self.user_repo.get_by_id(id)
        if not user:
            raise errors.NoUser(id=id)
        return user

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        new_user = user_info.create_obj(User)
        new_user = self.user_repo.add_instance(new_user)
        if self.publisher:
            self.publisher.plan(
                Message('ApiExchange',
                        {'obj_type': 'user',
                         'action': 'create',
                         'data': {'id_user': new_user.id,
                                  'name': new_user.user_name}
                         })
            )
        return new_user

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
    @validate_arguments
    def delete_user(self, id: int):
        user = self.user_repo.get_by_id(id)
        if not user:
            raise errors.NoUser(id=id)
        self.user_repo.delete_instance(id)
        if self.publisher:
            self.publisher.plan(
                Message('ApiExchange',
                        {'obj_type': 'user',
                         'action': 'delete',
                         'data': {'id_user': id}})
            )

    @join_point
    def get_all(self) -> List[User]:
        users = self.user_repo.get_all()
        return users
