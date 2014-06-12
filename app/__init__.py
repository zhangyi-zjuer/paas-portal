# -*- coding: utf-8 -*-

import sys

from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user

from database import session as database_session

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')


@app.teardown_appcontext
def shutdown_session(exception=None):
    database_session.remove()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'


@app.before_request
def before_request():
    g.user = current_user
    if not current_user.is_authenticated():
        from app.user.forms import LoginForm

        g.form = LoginForm()


import views

from admin.views import mod as admin_module
from user.views import mod as user_module
from api.views import mod as api_module

app.register_blueprint(admin_module, url_prefix='/admin')
app.register_blueprint(user_module, url_prefix='/user')
app.register_blueprint(api_module, url_prefix='/api')
