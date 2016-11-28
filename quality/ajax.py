#!/usr/bin/env python
# coding=utf-8

import datetime

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

from const import *
 
from iface.inspectIface import InspectIface

from models import InspectReport
from forms import *


inspect_dict = {
    "IMATERIEL" : 1,
    "IPROCESS" : 2,
    "IFEEDING" : 3,
    "IBARREL" : 4,
    "IASSEMBLE" : 5,
    "IPRESSURE" : 6,
    "IFACADE" : 7
}

@dajaxice_register
def getInspect(request, cate):
    category = inspect_dict.get(cate, 0)
    reports = InspectReport.objects.filter(category=category).exclude(checkstatus=FINISHED)
    for report in reports:
        report.extra_dict = json.loads(report.extra)
    context = {
        "reports" : reports,
    }
    return render_to_string("quality/%s.html" % cate, context)


@dajaxice_register
def getMaterielItemsTable(request, id_work_order):
    cate = "IMATERIEL"
    category = inspect_dict.get(cate, 0)
    report = InspectReport.objects.filter(category=category). \
            filter(work_order__id=id_work_order)[0]
    if report:
        report.extra_dict = json.loads(report.extra)
        items = InspectItem.objects.filter(report__id=report.id)
        for item in items:
            item.extra_dict = json.loads(item.extra)

    context = {
        "report" : report,
        "items" : items,
    }
    
    return render_to_string("quality/reports/IMaterielReport.html", context)
     

@dajaxice_register
def updateMaterielItem(request, item_id, inspect_item_form, materiel_form):
    try:
        inspect_item_form = InspectItemForm(deserialize_form(inspect_item_form), \
                                           instance=InspectItem.objects.get(id=item_id))
        materiel_form = MaterielForm(deserialize_form(materiel_form), \
                                    instance=MaterielInspectItem.objects.get(base__id=item_id))
        if inspect_item_form.is_valid() and materiel_form.is_valid():
            materiel_form.save()

            checkstatus = inspect_item_form.cleaned_data["checkstatus"]
            checkuser = request.user.id
            checkdate = datetime.datetime.now()
            extra = inspect_item_form.cleaned_data["extra"]

            iface = InspectIface()
            iface.update_item(item_id, checkstatus, checkuser, checkdate, extra)
    except Exception, e:
        print e

    

@dajaxice_register
def addMaterielItem(request, item_form):
    pass

@dajaxice_register
def getFeedingItemsTable(request, id_work_order):
    context = {}
    html = render_to_string("quality/reports/IFeedingReport.html", context)
    ret = {
        "html" : html,
    }

    return simplejson.dumps(ret)
