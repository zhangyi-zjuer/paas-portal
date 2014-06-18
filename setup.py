# -*- coding: utf-8 -*-
# Created by zhangyi on 14-3-14.

from app.user.models import *
from app.monitor.models import init_db as init_monitor_db
import hashlib


def add_user(username, password):
    if len(User.query.filter(User.username == username).all()) > 0:
        print username + " already exisits"
        return

    user = User()
    user.username = username
    user.password = hashlib.md5(password.encode('utf-8')).hexdigest()

    user_session.add(user)
    user_session.commit()

    print 'add user: ' + username


def del_user(username):
    users = User.query.filter(User.username == username).all()
    for user in users:
        user_session.delete(user)
        print 'delete user: ' + username
    user_session.commit()


def setup():
    r = raw_input("If you have already setup, All Data will be removed. Do you want setup?(y/n) ").lower()
    while not r in ['y', 'n', 'yes', 'no']:
        r = raw_input("Please Enter correct character (y or n): ").lower()

    if 'y' in r:
        init_db()
        init_monitor_db()
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





