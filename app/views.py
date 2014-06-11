# -*- coding: utf-8 -*-
# Created by zhangyi on 14-3-18.
import os
from app import app
from flask import send_from_directory, redirect, url_for


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('admin.machines'))
