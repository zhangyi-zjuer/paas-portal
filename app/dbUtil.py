# -*- coding: utf-8 -*-
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
