# coding: UTF-8

from django.shortcuts import render, redirect

from const.forms import WorkOrderForm
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
    #inspect_report = InspectReport.objects.get(work_order__id=order_id)
    #materiel_report = MaterielReport.objects.get_or_create(base=inspect_report)

    #items = InspectItem.objects.filter(report=report).order_by("index")
    #
    #context = {
    #    "inspect_report": inspect_report,
    #    "materiel_report": materiel_report,
    #    "items": items
    #}
    print "cao cao cao"
    context = {}
    return render(request, "quality/reports/IMaterielReport.html", context)

def feedingViews(request):
    context = {}
    return render(request, "quality/Feeding.html", context)
