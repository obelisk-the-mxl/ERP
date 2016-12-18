# coding: UTF-8

from django.shortcuts import render, redirect

from const.forms import WorkOrderForm, SubWorkOrderForm
from const.models import WorkOrder
from quality.forms import *
from quality.models import *

def materielViews(request):
    work_order_form = WorkOrderForm()
    context = {
        "form": work_order_form
    }
    return render(request, "quality/Materiel.html", context)

def materielDetailViews(request, order_id):
    context = {}
    return render(request, "quality/reports/IMaterielReport.html", context)

def processingViews(request):
    work_order_form = WorkOrderForm()
    sub_order_form = SubWorkOrderForm()
    context = {
        "form": work_order_form,
        "sub_order_form": sub_order_form
    }
    return render(request, "quality/Processing.html", context)

def processingCompleteViews(request, sub_work_order):
    context = {}
    return render(request, "quality/ProcessingComplete.html", context)

def feedingViews(request):
    work_order_form = WorkOrderForm()
    sub_order_form = SubWorkOrderForm()
    context = {
        "form": work_order_form,
        "sub_order_form": sub_order_form
    }
    return render(request, "quality/Feeding.html", context)
