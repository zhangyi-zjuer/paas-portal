# -*- coding: utf-8 -*-
import os

BOOTSTRAP_SERVE_LOCAL = True
SECRET_KEY = 'Bon-Jovi-Have-a-Nice-Day'

PAAS_HOST = 'http://127.0.0.1:2667'

BasicAuth = {
    'username': 'paas',
    'password': '123456',
    'enable': False
}

basedir = os.path.abspath(os.path.dirname(__file__))

db_url = 'mysql://root:root@localhost/paas'
user_db_url = 'sqlite:///' + os.path.join(basedir, 'user.db')

GROUP_MODE = {
    0: "Exclusive",
    1: "Share",
    2: "Share",
    3: "Share",
}

INSTANCE_STATUA = {
    0: "Running",
    1: "Deploying",
    2: "Deleting"
}

INSTANCE_STATUA_1 = {
    0: "NEW",
    100: "CREATING",
    101: "SHUTTINGDOWN",
    102: "STARTING",
    103: "REMOVING",
    200: "RUNNING",
    400: "REMOVED",
    500: "SHUTDOWN",
    501: "CREATE_FAIL",
    502: "ONLINE_FAIL",
    503: "UPGRADE_FAIL",
    504: "SHUTDOWN_FAIL",
    505: "START_FAIL",
    506: "REMOVE_FAIL",

}