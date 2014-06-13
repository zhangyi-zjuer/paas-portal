# -*- coding: utf-8 -*-

import json
import re

from flask import Blueprint, redirect, url_for, render_template, request
from flask.ext.login import login_required

from app.models import *
from app.admin.forms import *
from app.database import DbUtil
from app.paasUtil import format_num
from config import GROUP_MODE, INSTANCE_STATUA, INSTANCE_STATUA_1


mod = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@mod.route('/', methods=['GET'])
def index():
    redirect(url_for('admin.machines'))


@mod.route('/machines', methods=['GET', 'POST'])
def machines():
    form = MachineSearchForm()
    if request.method == 'GET':
        machines = Machine.query.all()

    else:
        ip = form.ip.data.strip()
        if not ip:
            machines = Machine.query.all()
        else:
            machines = Machine.query.filter(Machine.ip == ip).all()

    for machine in machines:
        machine.basic, machine.instances, machine.groups = get_agent_info(machine.agent)
        machine.format_disk = format_num(machine.disk)
        machine.format_memory = format_num(machine.memory)

    return render_template('machine.html', machines=machines, form=form)


@mod.route('/machine/add', methods=['GET', 'POST'])
@login_required
def add_machine():
    return edit_machine()


@mod.route('/machine/<machine_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_machine(machine_id=None):
    form = MachineForm()
    machine = Machine()
    if machine_id:
        machine = Machine.query.filter(Machine.id == machine_id)[0]

    if request.method == 'GET':
        if machine_id:
            form = get_form_from_db(machine, MachineForm())

        return render_template('form_template.html', form=form)

    if not form.validate_on_submit():
        return render_template('form_template.html', form=form)
    add_form_data_to_db(machine, form)

    return redirect(url_for('admin.machines'))


@mod.route('/machine/<machine_id>/delete', methods=['GET'])
@login_required
def del_machine(machine_id):
    DbUtil.delete(Machine.query.filter(Machine.id == machine_id).all())
    return redirect(url_for('admin.machines'))


@mod.route('/machine/<machine_id>/agent')
def show_agent(machine_id):
    machine = Machine.query.filter(Machine.id == machine_id)[0]
    basic, instances, groups = get_agent_info(machine.agent)
    return render_template("agent.html", machine=machine, basic=basic, instances=instances, groups=groups)


@mod.route('/instances', methods=['GET', 'POST'])
def instances():
    form = InstanceSearchForm()
    if request.method == 'GET':
        query = Instance.query
    else:
        type = form.type.data
        value = form.value.data
        if value:
            if type == 0:
                query = Instance.query.filter(Instance.agent_ip == value)
            else:
                app_info = re.split(r'\s*:\s*', value)
                query = Instance.query.filter(Instance.app_id.startswith(app_info[0]))
                if len(app_info) == 2:
                    query = query.filter(Instance.app_version == app_info[1])
        else:
            query = Instance.query

    instances = query.all()

    app_id_set = set()

    for instance in instances:
        app_id_set.add(instance.app_id)
        instance.status_desc = INSTANCE_STATUA_1[instance.status]
        if instance.agent_ip:
            instance.machine_id = Machine.query.filter(Machine.ip == instance.agent_ip)[0].id

    app_ids = '["' + '","'.join(app_id_set) + '"]'

    return render_template("instance.html", instances=instances, form=form, app_ids=app_ids)


@mod.route('/networks')
def networks():
    return render_template('network.html', networks=Network.query.all())


@mod.route('/network/add', methods=['GET', 'POST'])
@login_required
def add_network():
    return edit_network()


@mod.route('/network/<network_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_network(network_id=None):
    form = NetworkForm()
    network = Network()
    if network_id:
        network = Network.query.filter(Network.id == network_id)[0]

    if request.method == 'GET':
        if network_id:
            form = get_form_from_db(network, NetworkForm())
        return render_template('form_template.html', form=form)

    if not form.validate_on_submit():
        return render_template('form_template.html', form=form)
    add_form_data_to_db(network, form)

    return redirect(url_for('admin.networks'))


@mod.route('/network/<network_id>/del', methods=['GET', 'POST'])
@login_required
def del_network(network_id):
    DbUtil.delete(Network.query.filter(Network.id == network_id).all())
    return redirect(url_for('admin.networks'))


def add_form_data_to_db(obj, form):
    for attr in [attr for attr in dir(form) if hasattr(getattr(form, attr), 'data')]:
        if attr not in ['__class__', 'csrf_token'] and hasattr(obj, attr):
            setattr(obj, attr, getattr(form, attr).data)

    DbUtil.add(obj)


def get_form_from_db(obj, form):
    for attr in [attr for attr in dir(obj)]:
        if attr not in ['__class__', 'csrf_token'] and hasattr(form, attr) and hasattr(getattr(form, attr), 'data'):
            setattr(getattr(form, attr), 'data', getattr(obj, attr))
    return form


def get_agent_info(agent):
    if agent and len(agent) > 10:
        agent = json.loads(agent)

        basic = {
            'cpu': agent['cpu'],
            'memory': format_num(agent['memory']['total']),
            'memory_free': format_num(agent['memory']['free']),
            'disk': format_num(agent['disk']['total']),
            'disk_free': format_num(agent['disk']['free']),
            'ip': agent['ip']
        }

        cpu_groups = []
        m_cores = {}
        for group in agent['groups']:
            cpu_groups.append({
                'group_id': group['groupId'],
                'mode': GROUP_MODE[group['mode']],
                'max_instance': group['maxInstance'],
                'core': group['cores'],
                'core_str': ', '.join(map(str, group['cores']))
            })

            m_cores[group['groupId']] = ', '.join(map(str, group['cores']))

        instances = []

        for instance in agent['instances']:
            instances.append({
                'id': instance['id'],
                'ip': instance['ip'],
                'status': INSTANCE_STATUA[instance['status']],
                'token': instance['token'],
                'group_id': instance['groupId'],
                'cores': m_cores[instance['groupId']],
                'app_id': instance['app']['appId'],
                'app_version': instance['app']['appVersion'],
                'app_level': instance['app']['appLevel'],
                'cpu': instance['app']['cpuNum'],
                'cpu_mode': GROUP_MODE[instance['app']['cpuMode']],
                'memory': format_num(instance['app']['memorySize']),
                'disk': format_num(instance['app']['diskSize'])

            })

        basic['instance_num'] = len(instances)

        core_free = range(0, agent['cpu'])
        for group in cpu_groups:
            core_free = [core for core in core_free if core not in group['core']]

        basic['cpu_free'] = ', '.join(map(str, core_free))
        basic['cpu_free_num'] = len(core_free)

        return basic, instances, cpu_groups
    return None, None, None
