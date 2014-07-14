# -*- coding: utf-8 -*-
# Created by zhangyi on 14-3-14.

import hashlib
from optparse import OptionParser

from app.models.local import User, CatServerNameMap, InstanceOperator
import app.utils.dbUtil as DbUtil


def add_user(username, password):
    if len(User.query.filter(User.username == username).all()) > 0:
        print username + " already exisits"
        return

    user = User()
    user.username = username
    user.password = hashlib.md5(password.encode('utf-8')).hexdigest()

    DbUtil.add(user)

    print 'add user: ' + username


def del_user(username):
    users = User.query.filter(User.username == username).all()
    DbUtil.delete(users)

    print 'delete user: ' + username


def change_password(username, password):
    users = User.query.filter(User.username == username).all()

    if not users:
        print 'no user named: ' + username
        return

    for user in users:
        user.password = password

    print "%s password changed" % username
    DbUtil.add(users)


def setup():
    r = raw_input("If you have already setup, All Data will be removed. Do you want setup?(y/n) ").lower()
    while not r in ['y', 'n', 'yes', 'no']:
        r = raw_input("Please Enter correct character (y or n): ").lower()

    if 'y' in r:
        DbUtil.init_table(User)
        DbUtil.init_table(CatServerNameMap)
        DbUtil.init_table(InstanceOperator)
        print 'Set up Successfully'
    else:
        print 'Nothing Changed'


def get_optparser():
    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username",
                      help="specify the USERNAME", metavar="USERNAME")

    parser.add_option("-p", "--password", dest="password",
                      help="specify the PASSWORD", metavar="PASSWORD")

    parser.add_option("", "--add_user", action='store_true',
                      dest="add_user", default=False,
                      help="add a new user")

    parser.add_option("", "--del_user", action='store_true',
                      dest="del_user", default=False,
                      help="delete user")

    parser.add_option("-c", "--chg_pwd", action='store_true',
                      dest="chg_pwd", default=False,
                      help="change password")

    parser.add_option("", "--init_table", dest="table",
                      help="init table", metavar="TABLE_MODEL")

    parser.add_option("", "--init",
                      action="store_true", dest="init", default=False,
                      help="init the project")

    return parser


def init_table(table_classname):
    DbUtil.init_table(eval(table_classname))
    print 'Init %s success' % table_classname


if __name__ == "__main__":
    parser = get_optparser()
    (options, args) = parser.parse_args()

    username = options.username
    password = options.password
    is_init = options.init
    is_add_user = options.add_user
    is_del_user = options.del_user
    is_change_password = options.chg_pwd
    table = options.table


if is_init:
    setup()
    add_user('paas', '123456')
elif is_add_user:
    if username and password:
        add_user(username, password)
    else:
        print 'Please specify USERNAME and PASSWORD'
elif is_del_user:
    if username:
        del_user(username)
    else:
        print 'Please specify USERNAME'
elif is_change_password:
    if username and password:
        change_password(username, password)
    else:
        print 'Please specify USERNAME and PASSWORD'
elif table:
    init_table(table)
else:
    parser.print_help()
