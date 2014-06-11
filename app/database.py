# -*- coding: utf-8 -*-
# Created by zhangyi on 14-3-14.
import collections

from dbUtil import generate_db
from config import db_url


engine, session, Base = generate_db(db_url)


class DbUtil:
    def __init__(self):
        pass

    @staticmethod
    def __op__(obj, op_type):
        if not obj:
            return

        if isinstance(obj, collections.Iterable):
            for ele in obj:
                getattr(session, op_type)(ele)
        else:
            getattr(session, op_type)(obj)

        session.commit()

    @staticmethod
    def add(obj):
        DbUtil.__op__(obj, 'add')

    @staticmethod
    def delete(obj):
        DbUtil.__op__(obj, 'delete')
