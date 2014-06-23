# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-18.

from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField, BooleanField
from wtforms.validators import Required

from app.servers.monitor.util import *


class MonitorForm(Form):
    date = TextField('type', description='Enter Date')
    type = SelectField('type')
    hour = SelectField('type', coerce=int, choices=[(-1, 'All Hour')] + zip(range(0, 24), range(0, 24)), default=-1)
    percent = TextField('percent', description='Percent (default 0.1)')
    only_overload = BooleanField('overload', description="Only Overload", default=False)
    submit_button = SubmitField('Search')


class CatMapForm(Form):
    cat_name = TextField('catName', description='Enter Cat Name', validators=[Required()])
    real_name = SelectField('realName', choices=[])

    submit_button = SubmitField('Add')


