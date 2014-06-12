# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-12.
import time
from flask_login import login_required
from flask import Blueprint, request, redirect, url_for

from config import PAAS_HOST
from app.paasUtil import auth_request

mod = Blueprint('api', __name__, template_folder='templates', static_folder='static')


@mod.route('/instance/shutdown')
@login_required
def shutdown_instance():
    app_id = request.args.get('app_id')
    instance_id = request.args.get('instance_id')

    url = PAAS_HOST + '/console/api/instance?op=shutdown&appId=' + app_id + '&instanceId=' + instance_id

    response = auth_request(url)
    print response.read()

    time.sleep(0.5)
    return redirect(url_for('admin.instances'))


@mod.route('/instance/restart')
@login_required
def restart_instance():
    app_id = request.args.get('app_id')
    instance_id = request.args.get('instance_id')

    url = PAAS_HOST + '/console/api/instance?op=restart&appId=' + app_id + '&instanceId=' + instance_id

    response = auth_request(url)
    print response.read()

    time.sleep(0.5)
    return redirect(url_for('admin.instances'))