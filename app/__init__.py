# -*- coding: utf-8 -*-

import sys

from flask import Flask, g, session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user

from app.models.database import session as database_session
from app.models.local import session as local_session


reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')


@app.teardown_appcontext
def shutdown_session(exception=None):
    database_session.remove()
    local_session.remove()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'


@app.before_request
def before_request():
    session.modified = True
    g.user = current_user
    if not current_user.is_authenticated():
        from app.servers.user.forms import LoginForm

        g.form = LoginForm()


import views

from app.servers.admin.views import mod as admin_module
from app.servers.user.views import mod as user_module
from app.servers.api.views import mod as api_module
from app.servers.monitor.views import mod as monitor_module

app.register_blueprint(admin_module, url_prefix='/admin')
app.register_blueprint(user_module, url_prefix='/user')
app.register_blueprint(api_module, url_prefix='/api')
app.register_blueprint(monitor_module, url_prefix='/monitor')
