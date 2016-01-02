#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

from django.db.models import Q
from django.contrib.auth.models import User

from backend.utility import getContext
from forms import MaterielForm

from techdata.forms import MaterielForm, CirculationRouteForm
from techdata.models import *
from const.models import *

@dajaxice_register
def getProcessBOM(request, id_work_order):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    BOM = Materiel.objects.filter(order = work_order)
    for item in BOM:
        if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
            CirculationRoute(materiel_belong = item).save()
        item.route = '.'.join(getattr(item.circulationroute, "L%d" % i).name for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))
    context = {
        "work_order": work_order,
        "BOM": BOM,
    }
    html = render_to_string("techdata/widgets/processBOM_table.html", context)
    return html

@dajaxice_register  
def getMaterielInfo(request, iid):
    """
    JunHU
    """
    materiel = Materiel.objects.get(id = iid)
    form = MaterielForm(instance = materiel)
    circulationroute_form = CirculationRouteForm(instance = materiel.circulationroute)
    context = {
        "form": form,
        "circulationroute_form": circulationroute_form,
    }
    html = render_to_string("techdata/widgets/materiel_base_info.html", context)
    return html 

@dajaxice_register  
def getTechdataList(request, id_work_order):
    """
    MH Chen
    """
    workorder = WorkOrder.objects.filter(id = id_work_order)[0]
    materiel = Materiel.objects.filter(order = id_work_order)
    print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

    context = {
        "workorder": workorder,
        "materiel":materiel,
    }
    html = render_to_string("techdata/widgets/process_examination_table.html", context)
    return html

@dajaxice_register  
def getIndex(request, index):
    """
    MH Chen
    """
    materiel = Materiel.objects.filter(index = index)
    if len(materiel)==0:return
    form = MaterielForm(instance = materiel[0])
    context = {
        "form": form,
    }
    html = render_to_string("techdata/widgets/process_examination_table2.html", context)
    return html

@dajaxice_register
def getProcess(request, iid):
    """
    JunHU
    """
    materiel = Materiel.objects.get(id = iid)
    try:
        process = Processing.objects.get(materiel_belong = materiel, is_first_processing = True)  
        process_list = []
        while process:
            process_list.append(process)
            process = process.next_processing
    except:
        process_list = []
    
    context = {
        "process_list": process_list,
    }
    html = render_to_string("techdata/widgets/process_table.html", context)
    return html

@dajaxice_register
def addProcess(request, process_id, iid):
    """
    JunHU
    """
    materiel = Materiel.objects.get(id = iid)
    if Processing.objects.filter(materiel_belong = materiel).count() == 0:
        process = Processing(materiel_belong = materiel, name = process_id, is_first_processing = True)
        process.save()
    else:
        pre_process = Processing.objects.get(materiel_belong = materiel, next_processing = None)
        process = Processing(materiel_belong = materiel, name = process_id)
        process.save()
        pre_process.next_processing = process
        pre_process.save()

@dajaxice_register
def deleteProcess(request, pid):
    """
    JunHU
    """
    process = Processing.objects.get(id = pid)
    if process.is_first_processing == True:
        if process.next_processing:
            process.next_processing.is_first_processing = True
            process.next_processing.save()
        process.delete()
    else:
        pre_process = Processing.objects.get(next_processing = process)
        pre_process.next_processing = process.next_processing
        pre_process.save()
        process.delete()

@dajaxice_register
def getDesignBOM(request, id_work_order):
    """
    mxl
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    BOM = Materiel.objects.filter(order = work_order)
    for item in BOM:
        if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
            CirculationRoute(materiel_belong = item).save()
        item.route = '.'.join(getattr(item.circulationroute, "L%d" % i).name for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))
    context = {
        "work_order" : work_order,
        "BOM" : BOM,
    }
    html = render_to_string("techdata/widgets/designBOM_table.html", context)
    return html

@dajaxice_register
def getDesignBOMForm(request, iid):
    """
    mxl
    """
    materiel = Materiel.objects.get(id = iid)
    circulationroute = CirculationRoute.objects.filter(materiel_belong = iid)[0]
    materiel_form = MaterielForm(instance = materiel)
    circulationroute_form = CirculationRouteForm(instance = circulationroute)
    materiel_form_html = render_to_string("techdata/widgets/designBOM_materiel_form.html", {'materiel_form' : materiel_form})
    circulationroute_form_html = render_to_string("techdata/widgets/designBOM_circulationroute_form.html", {'circulationroute_form' : circulationroute_form})
    return simplejson.dumps({'materiel_form' : materiel_form_html, 'circulationroute_form' : circulationroute_form_html})

@dajaxice_register
def boxOutBought(request, boxoutbought):
    """
    BinWu
    """
    list = Materiel.objects.all();
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/tech_box_outbought_table.html", context)
    return html
