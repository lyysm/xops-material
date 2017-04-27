#!/usr/bin/python
# coding=utf-8

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'show_idc', views.show_idc, name='show_idc'),
]