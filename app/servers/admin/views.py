# -*- coding: utf-8 -*-

import re

from flask import Blueprint, redirect, url_for, render_template, request
from flask.ext.login import login_required

import app.utils.dbUtil as DbUtil
from app.models.database import *
from app.servers.admin.forms import *
from app.utils.paasUtil import format_num, get_agent_info, send_head_request
from config import INSTANCE_STATUA_1


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
        machine.is_running = True if send_head_request(machine.ip + ':8080', '/') == 200 else False

    ips = '["' + '","'.join([machine.ip for machine in Machine.query.all()]) + '"]'

    return render_template('machine.html', machines=machines, form=form, ips=ips)


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

    if request.method == 'POST':
        type, value, status = form.type.data, form.value.data, form.status.data
        return redirect(url_for('admin.instances', type=type, value=value, status=status))

    type, value, status = request.args.get('type'), request.args.get('value'), request.args.get('status') or -1

    query = Instance.query if request.args.get("all") or (type is not None and not value) else None

    if value and type is not None:
        type = int(type)
        if type == 0:
            query = Instance.query.filter(Instance.agent_ip == value)
        else:
            app_info = re.split(r'\s*:\s*', value)
            query = Instance.query.filter(Instance.app_id.startswith(app_info[0]))
            if len(app_info) == 2:
                query = query.filter(Instance.app_version == app_info[1])

    instances = query.order_by('instance_group_id').all() if query else []

    total, status_choice, s = 0, [(-1, 'All')], set()

    for instance in Instance.query.all():
        if instance.status in s:
            continue

        s.add(instance.status)
        status_choice.append((instance.status, INSTANCE_STATUA_1[instance.status]))

    statuses = {}
    for instance in instances:
        instance.status_desc = INSTANCE_STATUA_1[instance.status]

        instance.is_running = True if send_head_request(instance.instance_ip + ':8080', '/inspect/healthcheck') == 200 else False

        total += 1

        if not (instance.status, instance.status_desc) in statuses:
            statuses[(instance.status, instance.status_desc)] = 0

        statuses[(instance.status, instance.status_desc)] += 1

        if instance.agent_ip:
            instance.machine_id = Machine.query.filter(Machine.ip == instance.agent_ip)[0].id

    app_ids = '["' + '","'.join(set([instance.app_id for instance in Instance.query.all()])) + '"]'

    form.status.choices = [(-1, 'ALL')] + [ele[0] for ele in statuses.iteritems()] if statuses else status_choice
    form.type.data = int(type) if type not in [None, ''] else 1
    form.status.data = int(status) if status not in [None, ''] else -1
    form.value.data = value

    if not form.status.data in map(lambda d: d[0], status_choice):
        form.status.data = -1

    return render_template("instance.html", instances=instances, form=form, app_ids=app_ids,
                           total=total, statuses=statuses.iteritems())


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

