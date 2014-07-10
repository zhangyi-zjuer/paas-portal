# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-12.
import time
import datetime

from flask_login import login_required, current_user, request
from flask import Blueprint, request, redirect, url_for

from config import PAAS_HOST
from app.utils.paasUtil import auth_request


mod = Blueprint('api', __name__, template_folder='templates', static_folder='static')


@mod.route('/instance/shutdown')
@login_required
def shutdown_instance():
    return instance_op('shutdown')


@mod.route('/instance/start')
@login_required
def start_instance():
    return instance_op('start')


@mod.route('/instance/restart')
@login_required
def restart_instance():
    return instance_op('restart')


def instance_op(op):
    app_id = request.args.get('app_id')
    instance_id = request.args.get('instance_id')
    type = request.args.get('type')
    value = request.args.get('value')

    api_url = '/console/api/instance?op=' + op + '&appId=' + app_id + '&instanceId=' + instance_id
    auth_request(PAAS_HOST + api_url)

    time.sleep(0.5)

    add_to_db(api_url)

    if value:
        return redirect(url_for('admin.instances', type=type, value=value))

    return redirect(url_for('admin.instances', all="true"))


def add_to_db(request_url):
    from app.models.local import InstanceOperator
    import app.utils.dbUtil as DbUtil

    instance_operator = InstanceOperator()
    instance_operator.user = current_user.username
    instance_operator.ip = request.environ['REMOTE_ADDR']
    instance_operator.request = request_url
    instance_operator.timestamp = datetime.datetime.now()
    DbUtil.add(instance_operator)



