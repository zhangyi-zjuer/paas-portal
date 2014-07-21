# -*- coding: utf-8 -*-
# Created by zhangyi on 14-7-21.
import datetime
import app.utils.dbUtil as DbUtil
from app.models.local import Status
from app.utils.paasUtil import send_head_request, run_use_threadpool
from app.models.database import Machine, Instance
from sqlalchemy import and_


def get_machine_status(obj):
    obj.is_running = True if send_head_request(obj.ip + ':8080', '/') == 200 else False


def get_instance_status(obj):
    if obj.status != 200:
        obj.is_running = False
    else:
        obj.is_running = True if send_head_request(obj.instance_ip + ':8080',
                                                   '/inspect/healthcheck') == 200 else False


def fetch_machine_status():
    data = [machine for machine in Machine.query.all()]
    run_use_threadpool(get_machine_status, data, 10)
    statuses = []
    for machine in data:

        status = Status.query.filter(and_(Status.ip == machine.ip, Status.type == 'Machine')).all()
        if status:
            status = status[0]
        else:
            status = Status()
            status.ip = machine.ip
            status.type = 'Machine'

        status.update_time = datetime.datetime.now()
        status.is_running = machine.is_running
        statuses.append(status)

    DbUtil.add(statuses)


def fetch_instance_status():
    data = [instance for instance in Instance.query.all()]
    run_use_threadpool(get_instance_status, data, 100)
    statuses = []
    for instance in data:

        status = Status.query.filter(and_(Status.ip == instance.instance_ip, Status.type == 'Instance')).all()
        if status:
            status = status[0]
        else:
            status = Status()
            status.ip = instance.instance_ip
            status.type = 'Instance'

        status.update_time = datetime.datetime.now()
        status.is_running = instance.is_running
        statuses.append(status)

    DbUtil.add(statuses)


if __name__ == '__main__':
    fetch_machine_status()
    fetch_instance_status()





