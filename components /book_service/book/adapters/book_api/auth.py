import os

from classic.http_auth import Group, Permission, strategies


class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    USERS = Group('User', permissions=(Permissions.FULL_CONTROL, ))


jwt_strategy = strategies.JWT(
    secret_key=os.getenv('SECRET_KEY_JWT', 'my_secret_jwt')
)

ALL_GROUPS = (Groups.USERS, )
