from datetime import datetime
from unittest.mock import Mock

import pytest
from user.application import dataclasses, interfaces


@pytest.fixture(scope='function')
def user():
    return dataclasses.User(
        name='user_name_1', id=1, login='test', password='test'
    )


@pytest.fixture(scope='function')
def user_repo(user):
    user_repo = Mock(interfaces.UsersRepo)
    user_repo.get_by_id = Mock(return_value=user)
    user_repo.add_instance = Mock(return_value=user)
    user_repo.get_all = Mock(return_value=user)
    user_repo.get_by_login = Mock(return_value=user)
    return user_repo
