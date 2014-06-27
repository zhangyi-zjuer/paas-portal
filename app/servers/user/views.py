# coding:utf-8
import hashlib

from flask import Blueprint, redirect, url_for, g, flash, request, session
from flask.ext.login import login_user, logout_user, login_required

from app.models.local import User
from app import login_manager


mod = Blueprint('user', __name__, template_folder='templates', static_folder='static')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(redirect_url())

    form = g.form
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if len(username.strip()) == 0 or len(password.strip()) == 0:
            flash(u"Username or Password can't be blank !")

        user = User.query.filter_by(username=username).first()

        if not user:
            flash(u"Invalid User !")
            return redirect(redirect_url())

        if hashlib.md5(password.encode('utf-8')).hexdigest() == user.password:
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)

            login_user(user, remember=remember_me)
            return redirect(redirect_url())

        flash(u"Wrong username or password !")
        return redirect(redirect_url())

    flash(u"Please Enter your Username and Password !")
    return redirect(redirect_url())


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(redirect_url())


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def redirect_url():
    return request.args.get("next") or request.referrer or url_for('index')