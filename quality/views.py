# coding: UTF-8

from django.shortcuts import render, redirect

from const.forms import WorkOrderForm, SubWorkOrderForm
from const.models import WorkOrder
from quality.forms import *
from quality.models import *

def constViews(request):
    category_form = InspectCategoryForm()
    context = {
        "category_form": category_form
    }
    return render(request, "quality/ConstInput.html", context)

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

def processingCompleteViews(request, work_order_id):
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

def barrelViews(request):
    work_order_form = WorkOrderForm()
    sub_order_form = SubWorkOrderForm()
    context = {
        "form": work_order_form,
        "sub_order_form": sub_order_form
    }
    return render(request, "quality/Barrel.html", context)

def barrelReportDetailViews(request, sub_materiel):
    context = {}
    return render(request, "quality/reports/IBarrelReport.html", context)

def assembleViews(request):
    work_order_form = WorkOrderForm()
    sub_order_form = SubWorkOrderForm()
    context = {
        "form": work_order_form,
        "sub_order_form": sub_order_form
    }
    return render(request, "quality/Assemble.html", context)


def pressureViews(request):
    work_order_form = WorkOrderForm()
    sub_order_form = SubWorkOrderForm()
    context = {
        "form": work_order_form,
        "sub_order_form": sub_order_form
    }
    return render(request, "quality/Pressure.html", context)


def facadeViews(request):
    work_order_form = WorkOrderForm()
    sub_order_form = SubWorkOrderForm()
    context = {
        "form": work_order_form,
        "sub_order_form": sub_order_form
    }
    return render(request, "quality/Facade.html", context)
    
def finalViews(request):
    work_order_form = WorkOrderForm()
    sub_order_form = SubWorkOrderForm()
    context = {
        "form": work_order_form,
        "sub_order_form": sub_order_form
    }
    return render(request, "quality/Final.html", context)
    
def unpassViews(request):
    work_order_form = WorkOrderForm()
    context = {
        "form": work_order_form,
    }
    return render(request, "quality/UnPass.html", context)

def unqualityReportViews(request, bill_id):
    context = {}
    return render(request, "quality/reports/UnQuality.html", context)
   
def repairReportViews(request, bill_id):
    context = {}
    return render(request, "quality/reports/Repair.html", context)

def scrapReportViews(request, bill_id):
    context = {}
    return render(request, "quality/reports/Scrap.html", context)
