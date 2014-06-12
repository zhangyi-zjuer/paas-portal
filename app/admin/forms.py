# -*- coding: utf-8 -*-
# Created by zhangyi on 14-3-17.

from flask_wtf import Form
from wtforms import TextField, IntegerField, SubmitField, SelectField, HiddenField

from app.models import Network


class MachineForm(Form):
    agent = HiddenField('agent')
    version = IntegerField('version', default=1)
    cpu = IntegerField('cpu')
    ip = TextField('ip')
    memory = IntegerField('memory')
    disk = IntegerField('disk')
    idc = TextField('idc')
    switcher = TextField('swithcer')
    frame = TextField('frame')
    network_id = SelectField('network', coerce=int,
                             choices=[(network.id, network.id) for network in Network.query.all()])

    submit_button = SubmitField('OK')


class NetworkForm(Form):
    mask = IntegerField('mask')
    gateway = TextField('gateway')
    ip_pool = TextField('ip_pool')

    submit_button = SubmitField('OK')


class InstanceSearchForm(Form):
    type = SelectField('type', coerce=int, choices=[(0, 'Machine IP'), (1, 'App ID And Version')], default=0)
    value = TextField('value')
    submit_button = SubmitField('Search')


class MachineSearchForm(Form):
    ip = TextField('ip', description='Enter Machine IP')
    submit_button = SubmitField('Search')



