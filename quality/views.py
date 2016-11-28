# coding: UTF-8

from django.shortcuts import render, redirect

def materielReportView(request):
    context = {}
    return render(request, "quality/materielReport.html", context)

def feedingViews(request):
    context = {}
    return render(request, "quality/Feeding.html", context)
