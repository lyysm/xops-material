# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render_to_response
import urllib2
import json
import time
from django.conf import settings

from django.shortcuts import render

ALERT_SERVER = settings.ALERT_SERVER


# alert-list
def alert(request):
    # environments
    environments_result = json.loads(urllib2.urlopen(ALERT_SERVER + '/environments?status=open&status=unknown').read())
    # print environments_result
    environments_alert = environments_result['environments']
    for line in environments_alert:
        if line['environment'] == 'Production':
            count_production = line['count']
    # alert
    alert_result = json.loads(urllib2.urlopen(ALERT_SERVER + '/alerts?status=open&status=unknown').read())
    # print alert_result
    sum_alert = alert_result['total']
    for alert in alert_result['alerts']:
        lastReceiveTime = alert['lastReceiveTime'].replace('T', ' ')[:-5]
        alert['lastReceiveTime'] = lastReceiveTime
        alert['color'] = color(alert['severity'])
        print alert['color']
    return render(request, 'alert/alert.html', {'alert_list': alert_result['alerts']})


# top10
def top10(request):
    return render_to_response('alert/top10.html')


# details
def details(request):
    if request.method == 'GET':
        alertid = request.GET.get('id')
        # 拼接URL
        alert_url = "http://127.0.0.1:8080/alert/" + alertid
        details_result = json.loads(urllib2.urlopen(alert_url).read())
        alert_data = details_result['alert']
        alert_data['createTime'] = alert_data['createTime'].replace('T', ' ')[:-5]
        alert_data['receiveTime'] = alert_data['receiveTime'].replace('T', ' ')[:-5]
        alert_data['lastReceiveTime'] = alert_data['lastReceiveTime'].replace('T', ' ')[:-5]
        alert_data['color'] = color(alert_data['severity'])
        for line in alert_data['history']:
            update_time = line['updateTime'].replace('T', ' ')[:-5]
            line['updateTime'] = update_time
            if 'severity' in line:
                line['color'] = color(line['severity'])

    return render_to_response('alert/details.html', {'alertid': alertid, 'alert': alert_data})  # users


def users(request):
    return render_to_response('alert/users.html')


# about
def about(request):
    # status
    status_result = urllib2.urlopen(ALERT_SERVER + '/management/status').read()
    data = json.loads(status_result)
    # 版本信息
    api = data['application'] + "-" + data['version']
    # 秒数转换成时间
    minutes, seconds = divmod(data['uptime'] / 1000, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    up_time = "%d天%02d小时%02d分%02d秒" % (days, hours, minutes, seconds)
    # 当前时间
    app_time = time.localtime(data['time'] / 1000)
    now = time.strftime('%Y-%m-%d %H:%M:%S', app_time)
    manifest_result = urllib2.urlopen(ALERT_SERVER + '/management/manifest').read()
    print manifest_result
    info = json.loads(manifest_result)
    build = info['alerta']['build']
    print data['metrics']
    for i in data:
        print i
        print data.keys()
    return render(request, 'alert/about.html',
                  {'api': api, 'build': build, 'now': now, 'uptime': up_time, 'data': data['metrics']})


########### severity color --> zabbix ##############
# Critical      --> Disaster       --> deep orange
# Major         --> High           --> red
# Minor         --> Average        --> orange
# Warning       --> Warning        --> yellow
# Indeterminate --> Info           --> light blue
# Cleared       --> OK             --> light green
def color(Severity):
    COLOR = {'Critical': 'class=bg-deep-orange', 'Major': 'class=bg-red',
             'Minor': 'class=bg-orange', 'Warning': 'class=bg-yellow',
             'Indeterminate': 'class=bg-light-blue',
             'Cleared': 'class=bg-light-green', 'Unknow': 'class=bg-grey'}
    if Severity == 'Critical':
        c = COLOR['Critical']
    elif Severity == 'Major':
        c = COLOR['Major']
    elif Severity == 'Minor':
        c = COLOR['Minor']
    elif Severity == "Warning":
        c = COLOR['Warning']
    elif Severity == 'Indeterminate':
        c = COLOR['Indeterminate']
    elif Severity == 'Cleared':
        c = COLOR['Cleared']
    else:
        c = COLOR['Unknow']
    return c
