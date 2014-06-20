# coding:utf-8
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    username = TextField('Username', validators=[Required(message=u'Please Enter Username')])
    password = PasswordField('Password', validators=[Required(message=u'Please Enter Password')])
    remember_me = BooleanField('remember_me', default=True)