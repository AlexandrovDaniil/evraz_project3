from sqlalchemy import Column, Integer, MetaData, String, Table

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

BOOK = Table(
    'book',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author', String, nullable=True),
    Column('published_year', String, nullable=True),
    Column('title', String, nullable=True),
    Column('user_id', Integer, nullable=True),
)
