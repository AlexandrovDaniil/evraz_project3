from sqlalchemy import Column, Integer, MetaData, String, Table, BigInteger, Float, Boolean, DateTime, ForeignKey

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
    Column('isbn13', BigInteger, primary_key=True, autoincrement=True),
    Column('title', String(500)),
    Column('subtitle', String(500)),
    Column('authors', String(350)),
    Column('publisher', String(350)),
    Column('isbn10', String(35)),
    Column('tag', String(35)),
    Column('pages', Integer),
    Column('year', Integer),
    Column('rating', Integer),
    Column('desc', String(10000)),
    Column('price', Float),
    Column('bought', Boolean, default=False),
    Column('booking_time', DateTime, default=None),
    Column('timestamp', DateTime),
    Column('language', String(50)),
)

BOOK_HISTORY = Table(
    'book_history',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', BigInteger),
    Column('booking_time', DateTime),
    Column('user_id', Integer),
    Column('action', String),
)
