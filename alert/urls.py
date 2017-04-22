#!/usr/bin/python
# coding=utf-8

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.alert, name='alert'),
    url(r'top10', views.top10, name='top10'),
    url(r'about', views.about, name='about'),
    url(r'users', views.users, name='users'),
    url(r'details', views.details, name='details'),

]