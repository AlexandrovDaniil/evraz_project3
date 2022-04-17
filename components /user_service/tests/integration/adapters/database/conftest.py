import pytest
from evraz.classic.sql_storage import TransactionContext
from sqlalchemy import create_engine
from user.adapters.database.tables import metadata


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(
        'postgresql://postgres:password@localhost:5433/3rd_proj_integration_tests'
    )

    for key, value in metadata.tables.items():
        value.schema = None

    metadata.create_all(engine)

    return engine


@pytest.fixture(scope='session')
def transaction_context(engine):
    return TransactionContext(bind=engine)


@pytest.fixture(scope='function')
def session(transaction_context: TransactionContext):
    session = transaction_context.current_session

    if session.in_transaction():
        session.begin_nested()
    else:
        session.begin()

    yield session

    session.rollback()
