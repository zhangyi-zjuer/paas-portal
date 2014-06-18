# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-18.
from app.dbUtil import generate_db
from config import local_db_url
from sqlalchemy import CHAR, Column, INTEGER

engine, session, Base = generate_db(local_db_url)


class CatServerNameMap(Base):
    __tablename__ = 'cat_server_name_map'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(u'id', INTEGER, primary_key=True, autoincrement=True)
    cat_name = Column(u'cat_name', CHAR(length=128), nullable=False)
    real_name = Column(u'real_name', CHAR(length=128), nullable=False)


def init_db():
    CatServerNameMap.__table__.drop(engine, checkfirst=True)
    CatServerNameMap.metadata.create_all(bind=engine)