# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-4.
from app.dbUtil import generate_db
from config import local_db_url
from sqlalchemy import CHAR, Column

user_engine, user_session, User_Base = generate_db(local_db_url)


class User(User_Base):
    __tablename__ = 'user'
    __table_args__ = {}

    username = Column(u'username', CHAR(length=32), primary_key=True, nullable=False)
    password = Column(u'password', CHAR(length=32), nullable=False)

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


def init_table(table):
    table.__table__.drop(user_engine, checkfirst=True)
    table.metadata.create_all(bind=user_engine)


def init_db():
    init_table(User)
