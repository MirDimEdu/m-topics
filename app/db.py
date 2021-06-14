import uuid
import databases

from sqlalchemy import (create_engine, Table, Column, Integer, String, DateTime, MetaData,
                        ForeignKey)
from sqlalchemy.dialects.postgresql import UUID, TEXT
from datetime import datetime

from .config import cfg


_database = databases.Database(cfg.DB_CONNECTION_STRING) #, ssl=True)
_engine = create_engine(cfg.DB_CONNECTION_STRING)
_metadata = MetaData()


posts = Table('posts', _metadata,
    Column('id', Integer, primary_key=True),
    Column('account_id', Integer, nullable=False),
    Column('title', String, nullable=False),
    Column('text', String, nullable=False),
    Column('created', DateTime, default=datetime.utcnow, nullable=False)
)

comments = Table('comments', _metadata,
    Column('id', Integer, primary_key=True),
    Column('post_id', None, ForeignKey('posts.id')),
    Column('account_id', Integer, nullable=False),
    Column('text', String, nullable=False),
    Column('created', DateTime, default=datetime.utcnow, nullable=False)
)


def create_tables():
    print('Dropping existing tables', end='', flush=True)
    try:
        _metadata.reflect(_engine)
        _metadata.drop_all(_engine)
        print(' - OK')
    except Exception as e:
        print(f'Failed to drop tables.\n{str(e)}')
    print('Creating tables', end='', flush=True)
    _metadata.create_all(_engine)
    print(' - OK')
