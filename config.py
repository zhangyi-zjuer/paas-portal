# -*- coding: utf-8 -*-
import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
BOOTSTRAP_SERVE_LOCAL = True
SECRET_KEY = 'Bon-Jovi-Have-a-Nice-Day'

PAAS_HOST = 'http://127.0.0.1:2667'
PAAS_HOST_PREFIX = '10.101.'
CAT_HOST = '10.1.1.167'

# log config
LOG_FILE = os.path.join(basedir, 'log/portal.log')
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format=LOG_FORMAT)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)

BasicAuth = {
    'username': 'paas',
    'password': '123456',
    'enable': False
}

db_url = 'mysql://root:root@localhost/paas'
local_db_url = 'sqlite:///' + os.path.join(basedir, 'user.db')

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

