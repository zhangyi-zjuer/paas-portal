# -*- coding: utf-8 -*-
# Created by zhangyi on 14-3-14.

import hashlib

from app.models.local import session as local_session, User, CatServerNameMap
import app.utils.dbUtil as DbUtil


def add_user(username, password):
    if len(User.query.filter(User.username == username).all()) > 0:
        print username + " already exisits"
        return

    user = User()
    user.username = username
    user.password = hashlib.md5(password.encode('utf-8')).hexdigest()

    local_session.add(user)
    local_session.commit()

    print 'add user: ' + username


def del_user(username):
    users = User.query.filter(User.username == username).all()
    DbUtil.delete(users)

    print 'delete user: ' + username


def setup():
    r = raw_input("If you have already setup, All Data will be removed. Do you want setup?(y/n) ").lower()
    while not r in ['y', 'n', 'yes', 'no']:
        r = raw_input("Please Enter correct character (y or n): ").lower()

    if 'y' in r:
        DbUtil.init_table(User)
        DbUtil.init_table(CatServerNameMap)
        print 'Set up Successfully'
    else:
        print 'Nothing Changed'


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        setup()
        add_user('paas', '123456')
    elif len(sys.argv) == 4 and sys.argv[1] == 'add':
        add_user(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[1] == 'del':
        del_user(sys.argv[2])
