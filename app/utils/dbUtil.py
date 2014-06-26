# -*- coding: utf-8 -*-
import collections
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import compiler
from MySQLdb.converters import conversions, escape


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


def count(q):
    engine = q.session.bind
    q = str(compile_query(q))
    sql = "select count(*) " + q[q.lower().index("from"):]
    sql = sql.replace("%", "%%")

    return engine.execute(sql).fetchone()[0]


def compile_query(query):
    dialect = query.session.bind.dialect
    statement = query.statement
    comp = compiler.SQLCompiler(dialect, statement)
    comp.compile()
    enc = dialect.encoding
    params = []
    for k in comp.positiontup:
        v = comp.params[k]
        if isinstance(v, unicode):
            v = v.encode(enc)
        params.append(escape(v, conversions))
    return (comp.string.encode(enc) % tuple(params)).decode(enc)
