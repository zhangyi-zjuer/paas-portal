# -*- coding: utf-8 -*-
# Created by zhangyi on 14-6-18.

import xml.etree.ElementTree as ET
import urllib2
import time
import logging
import traceback

from config import CAT_HOST


def parse_report(xml_str):
    root = ET.fromstring(xml_str)
    machines = root.findall('report/machine')
    error_reports = []
    for machine in machines:
        ip = machine.get('ip')
        errors = []
        total_error_num = 0
        for error in machine.findall("entry[@type='error']"):
            error_num = int(error.find('duration').get('count'))
            errors.append({"status": error.get('status'), 'num': error_num})
            total_error_num += error_num

        error_reports.append({"ip": ip, "detail": errors, "total": total_error_num})

    return error_reports


def get_cat_error_report(domain, time):
    url = 'http://%s/cat/r/p?domain=%s&date=%s&forceDownload=xml' % (CAT_HOST, domain, time)
    try:
        request = urllib2.urlopen(url)
        return parse_report(request.read())
    except:
        logging.error('Cat request Exception: %s\n %s' % (domain, traceback.format_exc()))

    return None


def today():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


if __name__ == '__main__':
    error_reports = get_cat_error_report('FeedMQ', '2014061717')
    for report in error_reports:
        print report['ip'], report['total'], report['detail']

    print today()