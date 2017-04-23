# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render_to_response
import urllib2
import json, time

from django.shortcuts import render

# alert-list
def alert(request):
    # environments
    environments_result = json.loads(urllib2.urlopen('http://127.0.0.1:8080/environments?status=open&status=unknown').read())
    # print environments_result
    environments_alert = environments_result['environments']
    for line in environments_alert:
        if line['environment'] == 'Production':
            count_production = line['count']
    # alert
    alert_result = json.loads(urllib2.urlopen('http://127.0.0.1:8080/alerts?status=open&status=unknown').read())
    # print alert_result
    sum_alert = alert_result['total']
    print alert_result['alerts']
    for alert in alert_result['alerts']:
        lastReceiveTime = alert['lastReceiveTime'].replace('T', ' ')[:-5]
        alert['lastReceiveTime'] = lastReceiveTime
        alertid = alert['id']
        print alertid
    return render(request, 'alert/alert.html', {'alert_list': alert_result['alerts']})
# top10
def top10(request):
    return render_to_response('alert/top10.html')


# details
def details(request):
    if request.method == 'GET':
        alertid = request.GET.get('id')
        # 拼接URL
        alert_url = "http://127.0.0.1:8080/alert/"+alertid
        details_result = json.loads(urllib2.urlopen(alert_url).read())
        alert_data = details_result['alert']


        print details_result

    return render_to_response('alert/details.html',{'alertid':alertid, 'alert': alert_data})


# users
def users(request):
    return render_to_response('alert/users.html')


# about
def about(request):
    # status
    status_result = urllib2.urlopen('http://127.0.0.1:8080/management/status').read()
    data = json.loads(status_result)
    # 版本信息
    api = data['application'] + "-" + data['version']
    # 秒数转换成时间
    minutes, seconds = divmod(data['uptime']/1000, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours =  divmod(hours, 24)
    up_time = "%d天%02d小时%02d分%02d秒" % (days, hours, minutes, seconds)
    # 当前时间
    app_time = time.localtime(data['time']/1000)
    now = time.strftime('%Y-%m-%d %H:%M:%S', app_time)
    manifest_result = urllib2.urlopen('http://127.0.0.1:8080/management/manifest').read()
    print manifest_result
    info = json.loads(manifest_result)
    build = info['alerta']['build']
    print data['metrics']
    for i in data:
        print i
        print data.keys()
    return render(request, 'alert/about.html', {'api':api, 'build':build, 'now':now, 'uptime':up_time, 'data': data['metrics']})