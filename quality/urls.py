#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from quality import views as quality_views

urlpatterns=patterns(
    '',
    url(
        r'^materiel/$',
        quality_views.materielViews,
    ),
    url(
        r'^materiel_detail/(\w+)/$',
        quality_views.materielDetailViews,
    ),
    url(
        r'^feeding/$',
        quality_views.feedingViews,
    ),
)
