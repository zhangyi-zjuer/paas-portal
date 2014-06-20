# -*- coding: utf-8 -*-
import collections
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool


def generate_db(url):
    engine = create_engine(url, convert_unicode=True, poolclass=NullPool)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base = declarative_base()
    Base.query = session.query_property()
    return engine, session, Base


def db_operate(obj, op_type):
    if not obj:
        return
    session = obj.query.session
    if isinstance(obj, collections.Iterable):
        for ele in obj:
            getattr(session, op_type)(ele)
    else:
        getattr(session, op_type)(obj)
    session.commit()


def add(obj):
    db_operate(obj, 'add')


def delete(obj):
    db_operate(obj, 'delete')


def init_table(table):
    engine = table.query.session.bind
    table.__table__.drop(engine, checkfirst=True)
    table.metadata.create_all(bind=engine)
