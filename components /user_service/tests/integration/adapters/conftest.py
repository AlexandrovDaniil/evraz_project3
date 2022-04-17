from unittest.mock import Mock

import pytest
from falcon import testing
from user.adapters import user_api
from user.application import dataclasses, services


@pytest.fixture(scope='function')
def user():
    return dataclasses.User(
        id=1, name='Vasya', login='test_login1', password='test_pass1'
    )


@pytest.fixture(scope='function')
def users_service(user):
    service = Mock(services.Users)
    service.get_info = Mock(return_value=user)
    service.add_user = Mock(return_value=user)
    service.login_user = Mock(return_value=user)
    service.get_all = Mock(return_value=[user])
    return service


@pytest.fixture(scope='function')
def client(users_service):
    app = user_api.create_app(is_dev_mode=True, users=users_service)

    return testing.TestClient(app)
