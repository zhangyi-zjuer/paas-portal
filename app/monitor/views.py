# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-18.

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask.ext.login import login_required

from util import get_cat_error_report
from models import CatServerNameMap, session


mod = Blueprint('monitor', __name__, template_folder='templates', static_folder='static')


@mod.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    from forms import MonitorForm

    form = MonitorForm()
    form.type.choices = [('all', 'All Server')] + [(ele.cat_name, ele.cat_name) for ele in
                                                   CatServerNameMap.query.all()]
    servers = []
    if request.method == 'POST':
        type = form.type.data
        date = form.date.data
        hour = form.hour.data
        if hour == -1:
            hour = ''
        elif hour < 10:
            hour = '0' + str(hour)

        time = date.replace('-', '') + str(hour)

        if type != 'all':
            error_report = get_cat_error_report(type, time)
            servers.append({"name": type, "report": error_report})
        else:
            for server_name in CatServerNameMap.query.all():
                error_report = get_cat_error_report(server_name.cat_name, time)
                servers.append({"name": server_name.cat_name, "report": error_report})

    return render_template('index.html', servers=servers, form=form)


@mod.route('/cat', methods=['GET', 'POST'])
@login_required
def cat_name():
    from forms import CatMapForm

    form = CatMapForm()
    if request.method == 'GET':
        form.real_name.choices = get_not_selected()
        return render_template('cat.html', form=form, servers=CatServerNameMap.query.all())

    if len(form.cat_name.data.strip()) == 0:
        flash("'Cat Name' can't be blank!")
        form.real_name.choices = get_not_selected()
        return render_template('cat.html', form=form, servers=CatServerNameMap.query.all())

    cat_map = CatServerNameMap()
    cat_map.cat_name = form.cat_name.data
    cat_map.real_name = form.real_name.data
    session.add(cat_map)
    session.commit()

    form.real_name.choices = get_not_selected()
    return render_template('cat.html', form=form, servers=CatServerNameMap.query.all())


@mod.route('/cat/del/<id>')
@login_required
def del_cat(id):
    cat_names = CatServerNameMap.query.filter(CatServerNameMap.id == id).all()
    for cat_name in cat_names:
        session.delete(cat_name)
    session.commit()
    return redirect(url_for('monitor.cat_name'))


def get_not_selected():
    from app.models import AppVersion

    servers = sorted([ele.app_id for ele in AppVersion.query.all()])
    cats = [ele.real_name for ele in CatServerNameMap.query.all()]

    left = set()
    for server in servers:
        if not server in cats:
            left.add((server, server))

    return left







