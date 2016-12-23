#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from quality import views as quality_views

urlpatterns=patterns(
    '',
    url(
        r'^const/$',
        quality_views.constViews,
    ),
    url(
        r'^materiel/$',
        quality_views.materielViews,
    ),
    url(
        r'^materiel_detail/(\w+)/$',
        quality_views.materielDetailViews,
    ),
    url(
        r'^processing/$',
        quality_views.processingViews,
    ),
    url(
        r'^processing_complete/(\w+)/$',
        quality_views.processingCompleteViews,
    ),
    url(
        r'^feeding/$',
        quality_views.feedingViews,
    ),
    url(
        r'^barrel/$',
        quality_views.barrelViews,
    ),
    url(
        r'^barrel_detail/(\w+)/$',
        quality_views.barrelReportDetailViews,
    ),
    url(
        r'^assemble/$',
        quality_views.assembleViews,
    ),
    url(
        r'^pressure/$',
        quality_views.pressureViews,
    ),
)
