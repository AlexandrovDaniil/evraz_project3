import pytest
from attr import asdict

from user.adapters.database import tables
from user.adapters.database.repositories import UsersRepo
from user.application import dataclasses
from sqlalchemy.orm import registry


@pytest.fixture(scope='function')
def fill_db(session):
    users_data = [
        {
            'id': 1,
            'name': 'Vasya',
            'login': 'test_login1',
            'password': 'test_pass1',
        },
        {
            'id': 2,
            'name': 'Petya',
            'login': 'test_login2',
            'password': 'test_pass2',
        },
    ]

    session.execute(tables.USER.insert(), users_data)


@pytest.fixture(scope='function')
def mapping():
    mapper = registry()
    mapper.map_imperatively(dataclasses.User, tables.USER)


@pytest.fixture(scope='function')
def repo(transaction_context):
    return UsersRepo(context=transaction_context)


user_data_new = {
    'id': 3,
    'name': 'Vasya',
    'login': 'test_login1',
    'password': 'test_pass1',
}


def test__get_by_id(repo, fill_db):
    result = repo.get_by_id(user_id=1)
    assert result.id == 1


def test__add_instance(repo, fill_db):
    user = dataclasses.User(
        id=3,
        login='test_login1',
        password='test_pass1',
        name='Vasya'
    )
    result = repo.add_instance(user)
    assert asdict(result) == user_data_new


def test__get_all(repo, fill_db):
    result = repo.get_all()
    assert len(result) == 2


def test__get_by_login(repo, fill_db):
    result = repo.get_by_login(user_login='test_login1')
    assert result.id == 1
