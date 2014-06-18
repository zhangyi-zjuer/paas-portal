# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-18.

from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import Required

from models import CatServerNameMap
from util import *


class MonitorForm(Form):
    date = TextField('type', description='Enter Date', default=today())
    type = SelectField('type')
    hour = SelectField('type', coerce=int, choices=[(-1, 'All Hour')] + zip(range(0, 24), range(0, 24)), default=-1)
    submit_button = SubmitField('OK')


class CatMapForm(Form):
    cat_name = TextField('catName', description='Enter Cat Name', validators=[Required()])
    real_name = SelectField('realName', choices=[])

    submit_button = SubmitField('Add')


