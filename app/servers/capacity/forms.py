# -*- coding: utf-8 -*-
# Created by zhangyi on 14-7-16.

from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField


class CreateInstanceForm(Form):
    app_id = SelectField('app_id', choices=[])
    app_version = SelectField('app_version', choices=[])
    num = TextField('num', description="Instance Number", default='1')
    submit_button = SubmitField('Create')