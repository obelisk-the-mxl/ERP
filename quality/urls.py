#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from quality import views as quality_views

urlpatterns=patterns(
    '',
    url(
        r'materielReport',
        quality_views.materielReportViews,
    ),
    url(
        r'^feeding$',
        quality_views.feedingViews,
    ),
)
