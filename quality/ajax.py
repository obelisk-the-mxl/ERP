#!/usr/bin/env python
# coding=utf-8

import datetime

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson
from django.db.models import Q
 
from iface.inspectIface import InspectIface

from const.forms import SubWorkOrderForm

from quality.models import  InspectReport, MaterielReport, UnPassBill, UnQualityGoodsBill, RepairBill, ScrapBill, \
        FeedingReport, InspectReportMark, InspectItemConst, AssembleReport, AssembleInspectItem, \
        PressureReport, PressureReportItem, PressureReportValue
from production.models import SubMateriel, ProcessDetail
from const import IMATERIEL, IPROCESS, IFEEDING, IBARREL, IASSEMBLE, IPRESSURE, IFACADE, \
        FINISHED, APPLYCARD_END, REFUNDSTATUS_CHOICES_END, BARREL_INSPECT_ITEMS, \
        INSPECT_MARK, MATERIEL_MANAGER_MARK, UNPASS_TYPE, UnQuality, Repair, Scrap
from quality.forms import InspectReportForm, InspectItemForm, MaterielReportForm, MaterielItemForm, \
        FeedingReportForm, FeedingInspectItemForm, BarrelReportForm, BarrelInspectItemForm, \
        InspectItemConstForm, AssembleReportForm, AssembleInspectItemForm

from storage.models import SteelMaterialApplyCard, SteelMaterialApplyCardItems, SteelMaterialRefundCard, BoardSteelMaterialRefundItems, BarSteelMaterialRefundItems,  \
        OutsideApplyCard, OutsideApplyCardItems, OutsideRefundCard, OutsideRefundCardItems

from quality.utility import *


inspect_dict = {
    "IMATERIEL" : IMATERIEL,
    "IPROCESS" : IPROCESS,
    "IFEEDING" : IFEEDING,
    "IBARREL" : IBARREL,
    "IASSEMBLE" : IASSEMBLE,
    "IPRESSURE" : IPROCESS,
    "IFACADE" : IFACADE
}

@dajaxice_register
def addInspectConst(request, const_form, cate):
    try:
        category = inspect_dict.get(cate)
        cnt = InspectItemConst.objects.filter(category=category).aggregate(Max('index'))['index__max']
        const_form = InspectItemConstForm(deserialize_form(const_form))
        const_obj = const_form.save(commit=False)
        const_obj.index = cnt + 1
        const_obj.category = category
        const_obj.save()
        ret = 0
    except:
        ret = 1
    return {"ret": ret}

@dajaxice_register
def deleteInspectConst(request, iid):
    try:
        del_const = InspectItemConst.objects.get(id=iid)
        const_items = InspectItemConst.objects.filter(category=del_const.category).filter(index > del_const.index)
        for item in const_item:
            item.index = item.index - 1
            item.save()
        del_const.delete()
        ret = 0
    except:
        ret =1
    return {"ret": ret}

@dajaxice_register
def getMaterielReportTable(request, id_work_order):
    """
    author:mxl
    summary:
    get report list of materiel inspect
    """
    cate = "IMATERIEL"
    category = inspect_dict.get(cate, 0)
    if id_work_order:
        reports = MaterielReport.objects.filter(base__work_order__id=id_work_order).exclude(is_finished=True)
    else:
        reports = MaterielReport.objects.filter(base__category=category).exclude(is_finished=True)
    for report in reports:
        report.extra_dict = json.loads(report.base.extra) if report.base.extra else {}
    context = {
        "reports": reports
    }
    data = render_to_string("quality/tables/reports/materiel_reports_table.html", context)
    ret = {
        "data": data
    }
    return ret

@dajaxice_register
def getMaterielItemsTable(request, id_work_order):
    """
    author:mxl
    summary:
    get item list of a report of given id_work_order
    """
    cate = "IMATERIEL"
    category = inspect_dict.get(cate, 0)
    report = MaterielReport.objects.get(base__work_order__id=work_order, base_categroty=category)
    report.base.extra_str = json.loads(report.base.extra) if report.base.extra else {}

    items = MaterielInspectItem.objects.filter(base_item__report__id=report.base.id)
    for item in items:
        item.extra_dict = json.loads(item.base.extra) if item.base.extra else {}

    context = {
        "report" : report,
        "items" : items,
    }

    data = render_to_string("quality/reports/IMaterielReport.html", context)
    ret = {
        "data": data
    }
    return ret

@dajaxice_register
def updateMaterielReport(request, id_work_order, inspect_report_form, materiel_report_form):
    """
    author:mxl
    summary:
    update materiel report
    """
    ret = {}
    try:
        inspect_report = InspectReport.objects.get(work_order__id=id_work_order)
        materiel_report = MaterielReport.objects.get(base__work_order__id=id_work_order)
        inspect_report_form = InspectReportForm(deserialize_form(inspect_report_form), \
                                               instance=inspect_report)
        materiel_report_form = MaterielReportForm(deserialize_form(materiel_report_form), \
                                                 instance=materiel_report)

        if inspect_report_form.is_valid() and materiel_report_from.is_valid():
            materiel_obj = materiel_report_form.save()
            inspect_obj = inspect_report_form.save(commit=False)
            inspect_obj.checkdate = datetime.datetime.now()
            inspect_obj.save()
            ret.update({
                "StatusCode": 0
            })
        else:
            ret.update({
                "StatusCode": 1
            })
    except:
        ret.update({
            "StatusCode":2
        })
    return ret
     

@dajaxice_register
def updateMaterielItem(request, item_id, inspect_item_form, materiel_form):
    """
    author:mxl
    summary:
    update materiel item
    """
    try:
        inspect_item_form = InspectItemForm(deserialize_form(inspect_item_form), \
                                           instance=InspectItem.objects.get(id=item_id))
        materiel_form = MaterielForm(deserialize_form(materiel_form), \
                                    instance=MaterielInspectItem.objects.get(base_item__id=item_id))
        if inspect_item_form.is_valid() and materiel_form.is_valid():
            checkstatus = inspect_item_form.cleaned_data["checkstatus"]
            checkuser = request.user.id
            checkdate = datetime.datetime.now()
            extra = inspect_item_form.cleaned_data["extra"]

            iface = InspectIface()
            iface.update_item(item_id, checkstatus, checkuser, checkdate, extra)

            materiel_form.save()
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except Exception, e:
        print e
        ret = {"StatusCode": 2}
    return ret

@dajaxice_register
def finishMaterielReport(request, work_order_id):
    category = inspect_dict.get(cate)
    try:
        report = InspectReport.objects.get(work_order__id=work_order_id, category=category)
        if check_report_canbe_finish(report):
            report.is_finished = True
            report.save()
            ret = 0
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}

@dajaxice_register
def get_subworkorder(request, order_id):
    """
    author: mxl
    summary:
    get all of unfinished sub work order of a work order
    """
    sub_order_form = SubWorkOrderForm(order_id=order_id)
    return render_to_string("quality/widgets/sub_order_form.html", {
        "sub_order_form": sub_order_form,
    })


@dajaxice_register
def getProcessingItemForm(request, iid):
    inspect_item = ProcessInspectItem.objects.get(id=iid).base_item
    form = InspectItemForm(instance=inspect_item)
    context = {
        "form": form,
    }
    return render_to_string("quality/forms/items/processing_form.html", context)

def getProcessDetail(sub_work_order):
    cate="IPROCESS"
    category = inspect_dict.get(cate)
    inspect_report = InspectReport.objects.get_or_create(
        work_order=sub_work_order.order,
        category=category
    )
    process_report = ProcessReport.objects.get_or_create(
        base=inspect_report,
        sub_work_order=sub_work_order
    )
    sub_materiels = SubMateriel.objects.filter(materiel_belong__order=sub_work_order.order).filter(sub_order=sub_work_order)
    i = 0
    items = []
    for sub_materiel in sub_materiels:
        process_details = ProcessDetail.objects.filter(sub_materiel_belong)
        for process_detail in process_details:
            inspect_item = InspectItem(index=i, report=inspect_report)
            inspect_item.save()
            process_inspect_item = ProcessInspectItem(
                base_item=inspect_item,
                process_detail=process_detail
            )
            process_inspect_item.save()
            i += 1
            items.append(process_inspect_item)

    return items, process_report

@dajaxice_register
def getProcessingItems(request, sub_work_order_id):
    """
    author:mxl
    summary:
    get list of processing item
    """
    items = []
    sub_work_order = SubWorkOrder.objects.get(id=sub_work_order_id)
    report = ProcessReport.get(sub_work_order__id=sub_work_order_id)
    try:
        sub_materiels = SubMateriel.objects.filter(materiel_belong__order=sub_work_order.order).filter(sub_order=sub_work_order)
        for sub_materiel in sub_materiels:
            processing_items = ProcessInspectItem.objects.filter(process_detail__sub_materiel_belong=sub_materiel) 
            for item in processing_items:
                if not item.add_to_unpass:
                    item.extra_str = json.loads(item.base_item.extra) if item.base_item.extra else {}
                    items.append(item)
        if not items:
            items, report = getProcessDetail(sub_work_order)
    except:
        items = []
    context = {
        "items": items,
        "report": report
    }
    html = render_to_string("quality/tables/items/processing_table.html")
    ret = {
        "html": html
    }
    return ret

@dajaxice_register
def updateProcessingReport(request, sub_work_order_id, inspect_report_form):
    """
    author:mxl
    summary:
    update processing inspect report
    """
    try:
        inspect_report_form = InspectReportForm(deserialize_form(inspect_item_form), \
                                               instance=InspectReport.objects.get(sub_work_order_id=sub_work_order_id))
        if inspect_report_form.is_valid():
            inspect_report_obj = inspect_report_form.save(commit=False)
            inspect_report.obj.checkddate = datetime.datetime.now()
            inspect_report_obj.save()
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except:
        ret = {"StatusCode": 2}
    return ret

@dajaxice_register
def updateProcessingItem(request, item_id, inspect_item_form):
    """
    author:mxl
    summary:
    update processing inspect item
    """
    try:
        inspect_item_form = InspectItemForm(deserialize_form(inspect_item_form), \
                                           instance=InspectItem.objects.get(id=item_id))
        if inspect_item_form.is_valid():
            checkstatus = inspect_item_form.cleaned_data["checkstatus"]
            checkuser = request.user.id
            checkdate = datetime.datetime.now()
            extra = inspect_item_form.cleaned_data["extra"]

            iface = InspectIface()
            iface.update_item(item_id, checkstatus, checkuser, checkdate, extra)
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except Exception, e:
        print e
        ret = {"StatusCode": 2}
    return ret


UnPass_DICT = {
    "repair": RepairBill,
    "unquality": UnQualityGoodsBill,
    "scrap": ScrapBill
}

@dajaxice_register
def addUnPassBill(request, process_detail_ids, bill_type):
    """
    author:mxl
    summary:
    add a scrap bill
    """
    success_ids = []
    bill_model = UnPass_DICT.get(bill_type, None)
    if bill_model is not None:
        for pid in process_detail_ids:
            try:
                process_detail = ProcessDetail.objects.get(id=pid).select_related("processname")
                materiel = Materiel.objects.get(id=process_detail.sub_materiel_belong.materiel_belong) \
                        .select_related("order")
                bill = bill_model.objects.create(process_detail=process_detail)
                bill.texture= materiel.material
                bill.weight=materiel.total_weight
                bill.schematic_index=materiel.schematic_index
                bill.processname=process_detail.processname.name
                bill.name=materiel.name
                bill.total_count += 1
                #if bill_type == "repair":
                #    bill.repair_count += 1
                #elif bill_type == "unquality":
                #    bill.unquality_count =+ 1
                #elif bill_type == "scrap":
                #    bill.scrap_count += 1
                bill.save()
                counter = UnpassCounter.objects.get_or_create(
                    work_order=materiel.order,
                    unpass_type=bill_type
                )
                counter.cnt = counter.cnt + 1
                counter.save()
                
                process_inspect_item = process_detail.processinspectitem
                process_inspect_item.add_to_unpass = True
                process_inspect_item.save()

                success_ids.append(pid)

                iface = InspectIface()
                checkuser = request.user.id
                checkdate = datetime.datetime.now()
                iface.update_item(process_inspect_item.base_item.id, CheckUnPass, checkuser, checkdate, {})
            except:
                pass
    ret = {
        "success_ids": success_ids,
        "cate": bill_type
    }
    return ret

@dajaxice_register
def finishProcessReport(request, sub_work_order_id):
    category = inspect_dict.get(cate)
    try:
        report = InspectReport.objects.get(work_order__subworkorder__id=sub_work_order_id, category=category, processreport__sub_work_order__id=sub_work_order_id)
        if check_report_canbe_finish(report):
            report.is_finished = True
            report.save()
            ret = 0
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}   

@dajaxice_register
def getProcessComplete(request, sub_work_order_id):
    """
    author: mxl
    summary:
    for a given sub_work_order, get the product complete date and the inspect complete date, 
    of each materiel of this sub_work_order
    """
    ret = {}
    sub_work_order = SubWorkOrder.objects.get(id=sub_work_order_id)
    materiels = sub_work_order.order.materiel_set.all()
    for materiel in materiels:
        date_list = []
        process_details = ProcessDetail.objects.filter(sub_materiel_belong__materiel_belong=materiel).filter(sub_materiel_belong__sub_order=sub_work_order).order_by("complete_process_date")
        
        for process_detail in process_details:
            process_date = process_detail.complete_process_date if process_detail.complete_process_date else ""
            inspect_item = process_detail.processinspectitem
            inspect_item = inspect_item.base_item.checkdate if inspect_item else ""
            date_list.append({
                "process_name": process_detail.processname,
                "process_date": process_date,
                "inspect_date": inspect+date
            })
        ret[materiel.name] = date_list
        return date_list

class FeedingItems(object):
    def __init__(self, count, material_code, specification, schematic_index, name):
        self.count = count
        self.real_mateiral_code = material_code
        self.real_specification = specification
        self.schematic_index = schematic_index
        self.name = name

    def set_count(self, count):
        self.count = count

    def setDrawByMateriel(self, materiel):
        self.draw_material_code = materiel.material
        self.draw_specification = materiels.specification

    def setDrawByItem(self, item):
        self.draw_material_code = item.draw_materiel_code
        self.draw_specification = item.drwa_specification

"""
author: mxl
summary: get items from SteelMaterialApplyCard
"""
def getSteelFeedingList(sub_work_order):
    applys = SteelMaterialApplyCardItems.objects.filter(work_order__id=sub_work_order.order.id).filter(apply_card__status=APPLYCARD_END)
    board_refunds = BoardSteelMaterialRefundItems.objects.filter(applyitem__in(applys)).filter(card_info__status=REFUNDSTATUS_CHOICES_END)
    bar_refunds = BarSteelMaterialRefundItems.objects.filter(applyitem__in(applys)).filter(card_info__status=REFUNDSTATUS_CHOICES_END)
    refunds = board_refunds + bar_refunds
    refund_map = {x.id:x for x in refunds}
    items = []
    for apply in applys:
        materiel = apply.submateriel.materiel_belong
        item = FeedingItems(apply.count, apply.materiel_code, apply.specification, materiel.schematic_index, materiel.name)
        item.setDrawByMateriel(materiel)
        if apply.id in refund_map.keys():
            refund = refund_map.get(apply.id)
            if refund.count == apply.count:
                continue
            item.set_count(apply.count - refund.count)
            items.append(item)
        else:
            items.append(item)

    return items

"""
author: mxl
summary: get items from OutsideApplyCard
"""
def getOutsideFeedingList(sub_work_order):
    applys = OutsideApplyCardItems.objects.filter(apply_card__work_order=sub_work_order.order).filter(apply_card__statys=APPLYCARD_END)
    refunds = OutsideRefundCardItems.objects.filter(applyitem__in(applys)).filter(card_info__status=REFUNDSTATUS_CHOICES_END)
    refund_map = {x.id:x for x in refunds}
    items = []
    for apply in applys:
        materiel = apply.apply_card.submateriel.materiel_belong
        item = FeedingItems(apply.count, apply_materiel_code, apply.specification, materiel.schematic_index, materiel.name)
        item.setDrawByMateriel(materiel)
        if apply.id in refund_map.keys():
            refund = refund_map.get(apply.id)
            if refund.count == apply.count:
                continue
            item.set_count(apply.count - refund.count)
            items.append(item)
        else:
            items.append(item)

    return items

"""
author: mxl
summary: set the items get from applycard to database
"""
def setToFeedingDB(items, sub_work_order_id):
    sub_order = SubWorkOrder.objects.get(id=sub_work_order_id)
    cate = "IPROCESS"
    category = inspect_dict.get(cate)
    inspect_report = InspectReport.objects.get_or_create(
        work_order=sub_order.order,
        category=category
    )
    feeding_report = FeedingReport.objects.get_or_create(
        base=inspect_report,
        sub_work_order=sub_order,
        product_name=sub_order.order.product_name
    )
    mark_list = INSPECT_MARK.get(category)
    for mark in mark_list:
        materiel_manager_mark = InspectReportMark.objects.create(
            report=inspect_report,
            title=mark
        )
    for i, item in items.enumerate():
        inspect_item = InspectItem(
            report=feeding_report,
            index=i
        )
        inspect_item.save()
        process_item = ProcessInspectItem(
            base_item=inspect_item
        )
        process_item.save()

@dajaxice_register
def getFeedingItemsTable(request, sub_work_order_id):
    """
    author: mxl
    summary: get feeding inspect items by sub work_order_id
    """
    sub_work_order = SubWorkOrder.objects.get(id=sub_work_order_id)
    report = FeedingReport.objects.get(sub_work_order__id=sub_work_order_id)
    feeding_inspect_items = FeedingInspectItem.object.filter(base_item__report__work_order=sub_work_order.order)
    if not feeding_inspect_items:
        items = getSteelFeedingList(sub_work_order) + getOutsideFeedingList(sub_work_order)
        setToFeedingDB(items, sub_work_order_id)
    else:
        items = []
        for feeding_inspect_item in feeding_inspect_items:
            item = FeedingItems(feeding_inspect_item.amount,
                                feeding_inspect_item.real_texut,
                                feeding_inspect_item.real_specification,
                                feeding_inspect_item.schematic_index,
                                feeding_inspect_item.name)
            items.append(item)


    context = {
        "items": items,
        "report": report
    }
    html = render_to_string("quality/reports/IFeedingReport.html", context)
    ret = {
        "html" : html,
    }

    return simplejson.dumps(ret)

@dajaxice_register
def getFeedingItemForm(request, iid):
    feeding_inspect_item = FeedingInspectItem.object.get(id=iid)
    form = FeedingInspectItemForm(instance=feeding_inspect_item)
    return render_to_string("quality/forms/items/feeding_item_form.html")


@dajaxice_register
def getFeedingReportForm(request, sub_work_order_id):
    feeding_report = FeedingReport.objects.get(sub_work_order__id=sub_work_order_id)
    form = FeedingReportForm(instance=feeding_report)
    return render_to_string("quality/forms/reports/feeding_report_form.html")

@dajaxice_register
def updateFeedingReport(request, sub_work_order_id, inspect_report_form, feeding_report_form):
    """
    author:mxl
    summary:
    update feeding inspect report
    """
    try:
        inspect_report_form = InspectReportForm(deserialize_form(inspect_item_form), \
                                               instance=InspectReport.objects.get(sub_work_order_id=sub_work_order_id))
        feeding_report_form = FeedingReportForm(deserialize_form(feeding_item_form),
                                               instance=FeedingReport.objects.get(work_order__id=id_work_order))
        if inspect_report_form.is_valid() and feeding_report_form.is_valid():
            inspect_report_obj = inspect_report_form.save(commit=False)
            inspect_report.obj.checkddate = datetime.datetime.now()
            inspect_report_obj.save()
            feeding_report_form.save()
            
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except:
        ret = {"StatusCode": 2}
    return ret

@dajaxice_register
def updateFeedingItem(request, item_id, inspect_item_form, feeding_item_form):
    """
    author:mxl
    summary:
    update feeding inspect item
    """
    try:
        inspect_item_form = InspectItemForm(deserialize_form(inspect_item_form), \
                                           instance=InspectItem.objects.get(id=item_id))
        feeding_item_form = FeedingInspectItemForm(deserialize_form(feeding_item_form),
                                                  instance=FeedingInspectItem.object.get(base_item__id=item_id))
        if inspect_item_form.is_valid() and feeding_item_form.is_valid():
            checkstatus = inspect_item_form.cleaned_data["checkstatus"]
            checkuser = request.user.id
            checkdate = datetime.datetime.now()
            extra = inspect_item_form.cleaned_data["extra"]

            iface = InspectIface()
            iface.update_item(item_id, checkstatus, checkuser, checkdate, extra)
            feeding_item_form.save()
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except Exception, e:
        print e
        ret = {"StatusCode": 2}
    return ret

@dajaxice_register
def finishFeedingReport(request, sub_work_order_id):
    category = inspect_dict.get(cate)
    try:
        report = InspectReport.objects.get(work_order__subworkorder__id=sub_work_order_id, category=category, processreport__sub_work_order__id=sub_work_order_id)
        if check_report_canbe_finish(report):
            report.is_finished = True
            report.save()
            ret = 0
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}


def setMaterielManagerMark(request, sub_work_order_id):
    user = request.user
    report = InspectReport.objects.get(feedingreport__sub_work_order__id=sub_work_order_id)
    mark = InspectReportMark.objects.get(report=report, title=MATERIEL_MANAGER_MARK)
    mark.marker = user
    mark.markdate = datetime.datetime.now()
    mark.save()

def getBarrelMateriel(sub_work_order_id):
    """
    author:mxl
    summary:
    get barrel inspect item by transfer card in techdata
    """
    sub_order = SubWorkOrder.objects.get(id=sub_work_order_id).select_related("sub_materiel")
    sub_materiels = sub_order.submateriel_set.filter(sub_order=sub_order).filter(Q(sub_order__order__transfercard_card_type=CYLIDER_TRANSFER_CARD) | Q(sub_order__order__transfercard__card_type=CAP_TRANSFER_CARD))
    cate = "IBARREL"
    category = inspect_dict.get(cate)
    reports = []

    """
    get stipulate value
    """
    stipulate_values = []
    stipulates = InspectItemConst.objects.filter(category=category).order_by("index")
    for s in stipulates:
        stipulate_values.append(s.stipulate)

    for sub_materiel in sub_materiels:
        inspect_report = InspectReport.objects.get(
            work_order=work_order,
            category=category,
            barrelreport__sub_materiel=sub_materiel
        )
        
        if not inspect_report:
            inspect_report = InspectReport(
                work_order=work_order,
                category=category
            )
            inspect_report.save()
     
        barrel_report = BarrelReport.objects.get(
            base__work_order=work_order,
            sub_materiel=sub_materiel
        )

        if not barrel_report:
            barrel_report = BarrelReport(
                base=inspect_report,
                sub_materiel=sub_materiel
            )
            barrel_report.save()

        cnt = 0
        for i, group in enumerate(BARREL_INSPECT_ITEMS):
            process_name = group[0]
            process_detail = ProcessDetail.objects.get(processname__name=process_name,
                                                      sub_materiel=sub_materiel)
            items = group[1]
            for j, item in enumerate(items):
                index = cnt + j 
                
                stipulate = stipulate_values[index]
    
                inspect_item = InspectItem(
                    report=inspect_report,
                    index=index
                )
                inspect_item.save()
                barrel_item = BarrelInspectItem(
                    base_item=inspect_item, 
                    check_item=title_item,
                    process_detail=process_detail,
                    stipulate=stipulate
                )
                barrel_item.save()
            cnt += len(group)
        reports.append(barrel_report)
    return reports


def getBarrelReports(request, sub_work_order_id):
    reports = BarrelReport.objects.filter(sub_materiel__sub_order__id=sub_work_order_id)
    if not reports:
        reports = getBarrelReports(sub_work_order_id)
    context = {
        "reports": reports
    }
    return render_to_string("quality/tables/reports/barrel_reports_table.html") 


def getBarrelReportDetail(request, report_id):
    report = BarrelReport.objects.get(base__report__id=report_id).selet_related("barrelinspectitem")
    barrel_inspect_items = report.barrelinspectitem_set.all()
    context = {
        "items": barrel_inspect_items,
        "report": report
    }
    return render_to_string("quality/reports/IBarrelReport.html")

@dajaxice_register
def updateBarrelReport(request, sub_materiel_id, inspect_report_form, barrel_report_form):
    """
    author:mxl
    summary:
    update barrel inspect report
    """
    try:
        inspect_report_form = InspectReportForm(deserialize_form(inspect_item_form), \
                                               instance=InspectReport.objects.get(sub_materiel_id=sub_materiel_id))
        barrel_report_form = BarrelReportForm(deserialize_form(barrel_report_form), \
                                             instance=BarrelReport.objects.get(work_order__id=id_work_order))
        if inspect_report_form.is_valid() and barrel_report_form.is_valid():
            inspect_report_obj = inspect_report_form.save(commit=False)
            inspect_report.obj.checkddate = datetime.datetime.now()
            inspect_report_obj.save()
            barrel_report_form.save()
            
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except:
        ret = {"StatusCode": 2}
    return ret

@dajaxice_register
def updateBarrelItem(request, item_id, inspect_item_form, barrel_item_form):
    """
    author:mxl
    summary:
    update barrel inspect item
    """
    try:
        inspect_item_form = InspectItemForm(deserialize_form(inspect_item_form), \
                                           instance=InspectItem.objects.get(id=item_id))
        barrel_item_form = BarrelInspectItemForm(deserialize_form(barrel_item_form), \
                                                instance=BarrelInspectItem.objects.get(base_item__id=item_id))
        if inspect_item_form.is_valid() and barrel_item_form.is_valid():
            checkstatus = inspect_item_form.cleaned_data["checkstatus"]
            checkuser = request.user.id
            checkdate = datetime.datetime.now()
            extra = inspect_item_form.cleaned_data["extra"]

            iface = InspectIface()
            iface.update_item(item_id, checkstatus, checkuser, checkdate, extra)
            barrel_item_form.save()
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except Exception, e:
        print e
        ret = {"StatusCode": 2}
    return ret

def createAssembleItems(report, category):
    """
    the callback of create assemble items
    when barrel inspect is finished
    """
    const_items = InspectItemConst.objects.filter(category=category).order_by("index")
    for index, const_item in enumerate(const_items):
        inspect_item = InspectItem.objects.create(
            report=report,
            index=index
        )
        assemble_item = AssembleInspectItem.objects.create(
            base_item=inspect_item,
            check_item=const_item.check_item,
            stipulate=stipulate
        )

@dajaxice_register
def finishBarrelReport(request, sub_materiel_id):
    cate = "IASSEMBLE"
    category = inspect_dict.get(cate)
    try:
        report = InspectReport.objects.get(barrel__sub_materiel__id=sub_materiel_id)
        barrel_report = BarrelReport.objects.get(sub_materiel__id=sub_materiel_id).select_related("sub_materiel").select_related("base")
        report = barrel_report.base
        sub_work_order_id = barrel_report.sub_materiel.sub_order
        if check_report_canbe_finish(report):
            report.is_finished = True
            report.save()
            ret = 0
            afterFinish(sub_work_order_id, category, create_item_func=createAssembleItems)
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}

@dajaxice_register
def getAssembleItems(request, sub_work_order_id):
    report = AssembleReport.objects.get(sub_work_order__id=sub_work_order_id).select_related("base")
    inspect_items = report.base.inspectitem_set.all()
    items = map(lambda x: x.assembleinspectitem, inspect_items)
    context = {
        "items": items,
        "report": report
    }
    return render_to_string("quality/Assemble.html", context)


@dajaxice_register
def updateAssembleReport(request, sub_work_order_id, inspect_report_form, assemble_report_form):
    """
    author:mxl
    summary:
    update assemble inspect report
    """
    try:
        inspect_report_form = InspectReportForm(deserialize_form(inspect_item_form), \
                                               instance=InspectReport.objects.get(base__work_order__id=id_work_order))
        assemble_report_form = AssembleReportForm(deserialize_form(barrel_report_form), \
                                             instance=AssembleReport.objects.get(sub_work_order__id=sub_work_order_id))
        if inspect_report_form.is_valid() and assemble_report_form.is_valid():
            inspect_report_obj = inspect_report_form.save(commit=False)
            inspect_report.obj.checkddate = datetime.datetime.now()
            inspect_report_obj.save()
            assemble_report_form.save()
            
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except:
        ret = {"StatusCode": 2}
    return ret

@dajaxice_register
def updateBarrelItem(request, item_id, inspect_item_form, assemble_item_form):
    """
    author:mxl
    summary:
    update assemble inspect item
    """
    try:
        inspect_item_form = InspectItemForm(deserialize_form(inspect_item_form), \
                                           instance=InspectItem.objects.get(id=item_id))
        barrel_item_form = BarrelInspectItemForm(deserialize_form(barrel_item_form), \
                                                instance=AssembleInspectItem.objects.get(base_item__id=item_id))
        if inspect_item_form.is_valid() and barrel_item_form.is_valid():
            checkstatus = inspect_item_form.cleaned_data["checkstatus"]
            checkuser = request.user.id
            checkdate = datetime.datetime.now()
            extra = inspect_item_form.cleaned_data["extra"]

            iface = InspectIface()
            iface.update_item(item_id, checkstatus, checkuser, checkdate, extra)
            assemble_item_form.save()
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except Exception, e:
        print e
        ret = {"StatusCode": 2}
    return ret


def createPressureItems(report, category):
    items = PressureReportItem.objects.all().order_by("index")
    for item in items:
        value_item = PressureReportValue.objects.create(
            report=report,
            item=item
        )

@dajaxice_register
def finishAssembleReport(request, sub_work_order_id):
    cate = "IASSEMBLE"
    category = inspect_dict.get(cate)
    try:
        report = AssembleReport.objects.get(sub_work_order__id=sub_work_order_id)
        if check_report_canbe_finish(report):
            report.is_finished = True
            report.save()
            afterFinish(sub_work_order_id, category, create_item_func=createPressureItems)
            ret = 0
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}


@dajaxice_register
def getPressureReport(request, sub_work_order_id):
    report = PressureReport.objects.get(sub_work_order__id=sub_work_order_id).select_related("pressurereportvalue")
    items = report.pressurereportitem_set().all.select_related("pressurereportitem")
    for item in items:
        if item.has_stipulate:
            setattr(report, item.item.attr_name + "_stipulate", item.item.stipulate_value)
        setattr(report, item.item.attr_name, item.value)
    context = {
        "report": report
    }
    return render_to_string("quality/widgets/report/pressure_report.html")


@dajaxice_register
def getPressureReportForm(request, sub_work_order_id):
    form = PressureReportForm(instance=PressureReport.objects.get(sub_work_order__id=sub_work_order_id))
    return render_to_string("quality/forms/reports/pressure_report_form.html")

@dajaxice_register
def getPressureReportValueForm(request, sub_work_order_id):
    form = PressureReportValueForm()
    report = PressureReport.objects.get(sub_work_order__id=sub_work_order_id).select_related("pressurereportvalue")
    items = report.pressurereportitem_set.all().select_related("pressurereportitem")
    for item in items:
        if item.has_stipulate:
            setattr(form, item.item.attr_name + "_stipulate", item.item.stipulate_value)
        setattr(form, item.item.attr_name, item.value)
    return render_to_string("quality/forms/items/pressure_item_form.html")

@dajaxice_register
def updatePressureReport(request, sub_work_order_id, inspect_report_form, pressure_report_form):
    """
    author:mxl
    summary:
    update assemble inspect report
    """
    try:
        inspect_report_form = InspectReportForm(deserialize_form(inspect_item_form), \
                                               instance=InspectReport.objects.get(base__work_order__id=id_work_order))
        assemble_report_form = PressureReportForm(deserialize_form(barrel_report_form), \
                                             instance=PressureReport.objects.get(sub_work_order__id=sub_work_order_id))
        if inspect_report_form.is_valid() and pressure_report_form.is_valid():
            inspect_report_obj = inspect_report_form.save(commit=False)
            inspect_report.obj.checkddate = datetime.datetime.now()
            inspect_report_obj.save()
            pressure_report_form.save()
            
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except:
        ret = {"StatusCode": 2}
    return ret

@dajaxice_register
def updatePressureReportValueItem(request, item_id, sub_work_order_id, pressure_report_value_form):
    try:
        form = PressureReportValueForm(deserialize_form(pressure_report_value_form),
                                      instance=pressurereportvalue.objects.get(id=item_id))
        report = PressureReport.objects.get(sub_work_order__id=sub_work_order_id).select_related("pressurereportvalue")
        items = report.pressurereportitem_set
        if form.is_valid():
            for field in form.fields.keys():
                item = items.get(attr_name=field)
                v =form.cleaned_data.get(field)
                setattr(item, field, v)
                if field.endswith("_stipulate"):
                    pos = field.rfind("_stipulate")
                    sti_name = field[:pos]
                    stipulate_v = form.cleaned_data.get(sti_name)
                item.save()
            ret = 0
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}

@dajaxice_register
def setPressureInspectorMark(request, sub_work_order_id):
    user = request.user
    report = InspectReport.objects.get(pressurereport__sub_work_order__id=sub_work_order_id)
    mark = InspectReportMark.objects.get(report=report, title=INSPECTOR_MARK)
    mark.marker = user
    mark.markdate = datetime.datetime.now()
    mark.save()

@dajaxice_register
def setPressureInspectManaerMark(request, sub_work_order_id):
    user = request.user
    report = InspectReport.objects.get(pressurereport__sub_work_order__id=sub_work_order_id)
    mark = InspectReportMark.objects.get(report=report, title=INSPECT_MANAGER_MARK)
    mark.marker = user
    mark.markdate = datetime.datetime.now()
    mark.save()

@dajaxice_register
def setPressureManageMark(reques, sub_work_order_id):
    user = request.user
    report = InspectReport.objects.get(pressurereport__sub_work_order__id=sub_work_order_id)
    mark = InspectReportMark.objects.get(report=report, title=PRESSURE_MANAGER_MARK)
    mark.marker = user
    mark.markdate = datetime.datetime.now()
    mark.save()


def createFacadeItems(report, category):
    """
    the callback of create facade items
    when pressure inspect is finished
    """
    const_items = InspectItemConst.objects.filter(category=category).order_by("index")
    for index, const_item in enumerate(const_items):
        inspect_item = InspectItem.objects.create(
            report=report,
            index=index
        )
        facade_item = FacadeInspectItem.objects.create(
            base_item=inspect_item,
            check_item=const_item.check_item,
            stipulate=stipulate
        )

@dajaxice_register
def finishPressureReport(request, sub_work_order_id):
    cate = "IPRESSURE"
    category = inspect_dict.get(cate)
    try:
        report = PressureReport.objects.get(sub_work_order__id=sub_work_order_id)
        if check_report_canbe_finish(report):
            report.is_finished = True
            report.save()
            afterFinish(sub_work_order_id, category, create_item_func=createFacadeItems)
            ret = 0
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}

@dajaxice_register
def getFacadeReport(request, sub_work_order_id):
    report = FacadeReport.objects.get(sub_work_order__id=sub_work_order_id)
    items = report.FacadeInspectItem_set.all()
    context = {
        "report": report,
        "items": items
    }
    return render_to_string("quality/Facade.html")

@dajaxice_register
def getFacadeReportForm(request, sub_work_order_id):
    report_form = FacadeReportForm(
        instance=FacadeReport.objects.get(sub_work_order__id=sub_work_order_id)
    )
    context = {
        "report_form": report_form
    }
    return render_to_string("quality/forms/reports/facade_report_form.html", context)

@dajaxice_register
def getFacadeInspectItemForm(request, iid):
    item_form = FacadeInspectItemForm(
        instance=FacadeInspectItem.objects.get(id=iid)
    )
    context = {
        "item_form": item_form
    }
    return render_to_string("quality/forms/items/facade_item_form.html", context)

@dajaxice_register
def updateFacadeReport(request, sub_work_order_id, inspect_report_form, facade_report_form):
    """
    author:mxl
    summary:
    update assemble inspect report
    """
    try:
        inspect_report_form = InspectReportForm(deserialize_form(inspect_item_form), \
                                               instance=InspectReport.objects.get(base__work_order__id=id_work_order))
        assemble_report_form = FacadeReportForm(deserialize_form(barrel_report_form), \
                                             instance=FacadeReport.objects.get(sub_work_order__id=sub_work_order_id))
        if inspect_report_form.is_valid() and facade_report_form.is_valid():
            inspect_report_obj = inspect_report_form.save(commit=False)
            inspect_report.obj.checkddate = datetime.datetime.now()
            inspect_report_obj.save()
            facade_report_form.save()
            
            ret = {"StatusCode": 0}
        else:
            ret = {"StatusCode": 1}
    except:
        ret = {"StatusCode": 2}
    return ret

@dajaxice_register
def updatePressureReportValueItem(request, item_id, inspect_item_form, facade_item_form):
    try:
        inspect_item_form = InspectItemForm(deserialize_form(inspect_item_form),
                                           instance=InspectItem.objects.get(id=item_id))
        facade_item_form = FacadeInspectItemForm(deserialize_form(pressure_report_value_form),
                                    instance=FacadeInspectItem.objects.get(base_item__id=item_id))
        if inspect_item_form.is_valid() and facade_item_form.is_valid():
            checkstatus = inspect_item_form.cleaned_data["checkstatus"]
            checkuser = request.user.id
            checkdate = datetime.datetime.now()
            extra = inspect_item_form.cleaned_data["extra"]

            iface = InspectIface()
            iface.update_item(item_id, checkstatus, checkuser, checkdate, extra)
            facade_item_form.save()
            ret = 0
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}


@dajaxice_register
def setFacadeInspectManagerMark(request, sub_work_order_id):
    user = request.user
    report = InspectReport.objects.get(facadereport__sub_work_order__id=sub_work_order_id)
    mark = InspectReportMark.objects.get(report=report, title=INSPECT_MANAGER_MARK)
    mark.marker = user
    mark.markdate = datetime.datetime.now()
    mark.save()


def afterFinishFacade(sub_work_order_id):
    final_inspect = FinalInspect(sub_work_order__id=sub_work_order_id)
    final_inspect.save()

@dajaxice_register
def finishFacadeReport(request, sub_work_order_id):
    cate = "IFACADE"
    category = inspect_dict.get(cate)
    try:
        report = FacadeReport.objects.get(sub_work_order__id=sub_work_order_id)
        if check_report_canbe_finish(report):
            report.is_finished = True
            report.save()
            afterFinishFacade(sub_work_order_id)
            ret = 0
        else:
            ret = 1
    except:
        ret = 2
    return {"ret": ret}


@dajaxice_register
def getFinalInspects(request):
    retports = FinalInspect.objects.exclude(checkstatus=FINISHED)
    context = {
        "reports": reports
    }
    return render_to_string("quality/Final.html", context)

@dajaxice_register
def updateFinishInspect(request, sub_work_order_id, status):
    try:
        final_report = FinalInspect.objects.get(sub_work_order__id=sub_work_order_id)
        final_report.checkuser = request.user
        final_report.checkstatus=status
        final_report.checkdate = datetime.datetime.now()
        final_report.save()
        ret = 0
    except:
        ret = 1
    return {"ret": ret}


UNPASS_MODEL_DICT = {
    UnQuality: UnQualityGoodsBill,
    Repair: RepairBill,
    Scrap: ScrapBill
}

@dajaxice_register
def getUnPassList(request, work_order_id):
    for unpass_type, bill_model in UNPASS_MODEL_DICT.iteritems():
        bills = bill_model.objects.filter(
            process_detail__sub_materiel_belong__sub_order__order__id=work_order_id)
        counter = UnpassCounter.objects.get(
            work_order__id=work_order_id,
            unpass_type=unpass_type
        )
        for bill in bills:
            bill.signature_sheets = SignatureSheet.objects.filter(bill=bill)
        bill_dict[unpass_type] = bills
    context = {
        "bill_dict": bill_dict,
        "counter": counter
    }
    return render_to_string("quality/reports/%s_report.html" % unpass_type, context)


