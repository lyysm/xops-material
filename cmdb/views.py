# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from django.conf import settings

idc_ison = settings.IDC_JSON

def show_idc(request):
    DC_zw = {}
    DC_mjq = {}
    # 机柜U数
    Cabinet = []
    u = 10
    for u_num in range(0, u):
        u_num = "null"
        Cabinet.append(u_num)

    file = open(idc_ison, 'r')
    a = json.load(file)
    print '--------------------------------'
    print a
    for line in a:
        H = a[line]
        C = H["cabinet"]
        P = H["place"]
        if H["DataCenter"] == "zw":
            c_zw = ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null"]
            if C in DC_zw:
                DC_zw[C][int(P) - 1] = H
            else:
                DC_zw[C] = c_zw
                DC_zw[C][int(P) - 1] = H
        elif H["DataCenter"] == "mjq":
            c_mjq = ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null"]
            print c_mjq
            if C in DC_mjq:
                DC_mjq[C][int(P) - 1] = H
            else:
                DC_mjq[C] = c_mjq
                DC_mjq[C][int(P) - 1] = H

        else:
            print "error"
    zw_l = []
    mjq_l = []
    print DC_zw
    for d_key in DC_zw:
        d_list = [d_key, DC_zw[d_key]]
        # print d_list
        zw_l.append(d_list)

    for m_key in DC_mjq:
        m_list = [m_key, DC_mjq[m_key]]
        mjq_l.append(m_list)

    return render(request, "cmdb/show_idc.html", {"zw": zw_l, "mjq": mjq_l})