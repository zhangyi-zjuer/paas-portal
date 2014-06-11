# coding:utf-8
import hashlib

from flask import Blueprint, redirect, url_for, g, session, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user

from models import *
from app import login_manager


mod = Blueprint('user', __name__, template_folder='templates', static_folder='static')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(request.args.get("next") or url_for('index'))

    form = g.form
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if len(username.strip()) == 0 or len(password.strip()) == 0:
            flash(u"Username or Password can't be blank !")

        user = User.query.filter_by(username=username).first()

        if not user:
            flash(u"Invalid User !")
            return redirect(url_for('index'))

        if hashlib.md5(password.encode('utf-8')).hexdigest() == user.password:
            remember_me = True
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)

            login_user(user, remember=remember_me)
            print request.args.get("next")
            return redirect(request.args.get("next") or url_for('index'))

        flash(u"Wrong username or password !")
        return redirect(request.args.get("next") or url_for('index'))

    flash(u"Please Enter your Username and Password !")
    return redirect(request.args.get("next") or url_for('index'))


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)