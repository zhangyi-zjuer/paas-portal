# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-20.

from sqlalchemy import CHAR, Column, INTEGER, TIMESTAMP, TEXT, BOOLEAN
from app.utils.dbUtil import generate_db
from config import local_db_url


engine, session, Base = generate_db(local_db_url)


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {}

    username = Column(u'username', CHAR(length=32), primary_key=True, nullable=False)
    password = Column(u'password', CHAR(length=32), nullable=False)
    role = Column(u'role', INTEGER, default=0, nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<User %r>' % self.username


class CatServerNameMap(Base):
    __tablename__ = 'cat_server_name_map'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(u'id', INTEGER, primary_key=True, autoincrement=True)
    cat_name = Column(u'cat_name', CHAR(length=128), nullable=False)
    real_name = Column(u'real_name', CHAR(length=128), nullable=False)


class InstanceOperator(Base):
    __tablename__ = 'instance_operator'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(u'id', INTEGER, primary_key=True, autoincrement=True)
    ip = Column(u'ip', CHAR(length=128), nullable=False)
    user = Column(u'user', CHAR(length=128), nullable=False)
    timestamp = Column(u'timestamp', TIMESTAMP, nullable=False)
    request = Column(u'request', TEXT)


class Status(Base):
    __tablename__ = 'status'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(u'id', INTEGER, primary_key=True, autoincrement=True)
    ip = Column(u'ip', CHAR(length=64), nullable=False)
    type = Column(u'type', CHAR(length=32), nullable=False)
    is_running = Column(u'is_running', BOOLEAN, nullable=False)
    update_time = Column(u'update_time', TIMESTAMP, nullable=False)

