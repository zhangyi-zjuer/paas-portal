# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-9.
import json
import urllib2
import base64

from flask import url_for
from config import GROUP_MODE, INSTANCE_STATUA, BasicAuth
from app.models.database import *


def get_instances_by_app(app_id, app_version=None):
    satisfied_instances = []
    instances = []
    for machine in Machine.query.all():
        agent = machine.agent
        instances.extend(get_instances_by_agent(agent))

    for instance in instances:
        if app_id == instance['app_id'] and (not app_version or (app_version == instance['app_version'] )):
            satisfied_instances.append(instance)

    return satisfied_instances


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
                'id': instance['id'] if 'id' in instance else '',
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


def get_instances_by_agent(agent):
    instances = []
    if agent and len(agent) > 10:
        agent = json.loads(agent)
    else:
        return instances

    for instance in agent['instances']:
        instances.append({
            'machine': agent['ip'],
            'id': instance['id'],
            'ip': instance['ip'],
            'status': INSTANCE_STATUA[instance['status']],
            'token': instance['token'],
            'group_id': instance['groupId'],
            'app_id': instance['app']['appId'],
            'app_version': instance['app']['appVersion'],
            'app_level': instance['app']['appLevel'],
            'cpu': instance['app']['cpuNum'],
            'cpu_mode': GROUP_MODE[instance['app']['cpuMode']],
            'memory': instance['app']['memorySize'],
            'disk': instance['app']['diskSize']

        })

    return instances


def auth_request(url):
    request = urllib2.Request(url)
    if BasicAuth['enable']:
        username = BasicAuth['username']
        password = BasicAuth['password']
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
    return urllib2.urlopen(request)


def format_num(n):
    unit = ['', 'K', 'M', 'G', 'T', 'P']
    index = 0
    while n / 1024 >= 1 and index < len(unit) - 1:
        n = n * 1.0 / 1024
        index += 1
    return str('%.2f' % n) + unit[index]


def pagination(current_page, total_page, url_prefix='/', max=10, prev_tag='<', next_tag='>',
               hide_if_only_one_page=True):
    if current_page < 1 or current_page > total_page:
        return None

    if hide_if_only_one_page and total_page < 2:
        return None

    class Page:
        def __init__(self, text, href=None, clazz=""):
            self.text = text
            self.href = href
            self.clazz = clazz

    pages = []

    if max < 8:
        max = 8

    if max % 2 == 0:
        max += 1

    if current_page == 1:
        pages.append(Page(prev_tag, clazz='disabled'))
    else:
        pages.append(Page(prev_tag, url_for(url_prefix, page=current_page - 1)))

    if total_page <= max:
        for i in range(1, total_page + 1):
            page = Page(i, url_for(url_prefix, page=i))
            if i == current_page:
                page.clazz = 'active'
            pages.append(page)
    else:
        prev_num = current_page - 1
        next_num = total_page - current_page

        if prev_num > max / 2 and next_num > max / 2:
            pages.append(Page(1, url_for(url_prefix, page=1)))
            pages.append(Page('...', clazz='disabled'))
            for i in range(current_page - (max / 2 - 2), current_page):
                pages.append(Page(i, url_for(url_prefix, page=i)))

            pages.append(Page(current_page, url_for(url_prefix, page=current_page), 'active'))

            for i in range(current_page + 1, current_page + (max / 2 - 2) + 1):
                pages.append(Page(i, url_for(url_prefix, page=i)))

            pages.append(Page('...', clazz='disabled'))
            pages.append(Page(total_page, url_for(url_prefix, page=total_page)))

        elif prev_num > max / 2 and next_num <= max / 2:
            left_num = max - next_num - 1
            pages.append(Page(1, url_for(url_prefix, page=1)))
            pages.append(Page('...', clazz='disabled'))
            for i in range(current_page - (left_num - 2), current_page):
                pages.append(Page(i, url_for(url_prefix, page=i)))

            pages.append(Page(current_page, url_for(url_prefix, page=current_page), 'active'))
            for i in range(current_page + 1, total_page + 1):
                pages.append(Page(i, url_for(url_prefix, page=i)))
        else:
            for i in range(1, current_page):
                pages.append(Page(i, url_for(url_prefix, page=i)))
            pages.append(Page(current_page, url_for(url_prefix, page=current_page), 'active'))

            left_num = max - prev_num - 1
            for i in range(current_page + 1, current_page + (left_num - 2) + 1):
                pages.append(Page(i, url_for(url_prefix, page=i)))
            pages.append(Page('...', clazz='disabled'))
            pages.append(Page(total_page, url_for(url_prefix, page=total_page)))

    if current_page == total_page:
        pages.append(Page(next_tag, clazz='disabled'))
    else:
        pages.append(Page(next_tag, url_for(url_prefix, page=current_page + 1)))

    return pages
