# -*- coding: utf-8 -*-
# Created by zhangyi on 14-7-16.

import time
import datetime

from flask_login import login_required, current_user
from flask import Blueprint, request, redirect, url_for, render_template, flash

from config import PAAS_HOST
from app.utils.paasUtil import auth_request
from app.models.database import AppVersion
from forms import CreateInstanceForm


mod = Blueprint('capacity', __name__, template_folder='templates', static_folder='static')


@mod.route('/create', methods=['GET', 'POST'])
def create_instance():
    form = CreateInstanceForm()
    apps = {}
    for app in AppVersion.query.all():
        app_id = app.app_id
        app_version = app.version
        if not app_id in apps.keys():
            apps[app_id] = []

        if not app_version in apps[app_id]:
            apps[app_id].append(app_version.strip())

    for k, v in apps.iteritems():
        apps[k] = ",".join(sorted(v))

    form.app_id.choices = sorted([(ele, ele) for ele in apps.keys()])

    if request.method == 'GET':
        return render_template('create.html', form=form, apps=apps.iteritems())
    else:
        app_id = form.app_id.data
        app_version = form.app_version.data
        num = form.num.data
        try:
            num = int(num)
        except:
            num = 0

        if num <= 0:
            flash("Instance Number must be Integer and greater than 0")
            return render_template('create.html', form=form)

        return redirect(url_for('api.create_instance', appId=app_id, version=app_version, num=num))




