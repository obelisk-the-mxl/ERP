#!/usr/bin/env python
# coding=utf-8

import datetime

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

 
from iface.inspectIface import InspectIface

from const.forms import SubWorkOrderForm

from quality.models import InspectCategory, InspectReport, MaterielReport, UnPassBill, UnQualityGoodsBill, RepairBill, ScrapBill, \
        FeedingReport
from production.models import SubMateriel, ProcessDetail
from const import IMATERIEL, IPROCESS, IFEEDING, IBARREL, IASSEMBLE, IPRESSURE, IFACADE, \
        FINISHED, APPLYCARD_END, REFUNDSTATUS_CHOICES_END
from forms import InspectReportForm, InspectItemForm, MaterielReportForm, MaterielItemForm

from storage.models import SteelMaterialApplyCard, SteelMaterialApplyCardItems, SteelMaterialRefundCard, BoardSteelMaterialRefundItems, BarSteelMaterialRefundItems,  \
        OutsideApplyCard, OutsideApplyCardItems, OutsideRefundCard, OutsideRefundCardItems


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
def getMaterielReportTable(request, id_work_order):
    """
    author:mxl
    summary:
    get report list of materiel inspect
    """
    cate = "IMATERIEL"
    category = inspect_dict.get(cate, 0)
    if id_work_order:
        reports = MaterielReport.objects.filter(base__work_order__id=id_work_order).exclude(checkstatus=FINISHED)
    else:
        reports = MaterielReport.objects.filter(base__category__id=category).exclude(checkstatus=FINISHED)
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
    report = MaterielReport.objects.get(base__work_order__id=work_order, base_categroty__id=category)
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
    category = Category.objects.get(name="IPROCESS")
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

    return items

@dajaxice_register
def getProcessingItems(request, sub_work_order_id):
    """
    author:mxl
    summary:
    get list of processing item
    """
    items = []
    sub_work_order = SubWorkOrder.objects.get(id=sub_work_order_id)
    try:
        sub_materiels = SubMateriel.objects.filter(materiel_belong__order=sub_work_order.order).filter(sub_order=sub_work_order)
        for sub_materiel in sub_materiels:
            processing_items = ProcessInspectItem.objects.get(process_detail__sub_materiel_belong=sub_materiel) 
            for item in processing_items:
                if not item.add_to_unpass:
                    item.extra_str = json.loads(item.base_item.extra) if item.base_item.extra else {}
                    items.append(item)
        if not items:
            items = getProcessDetail(sub_work_order)
    except:
        items = []
    context = {
        "items": items
    }
    html = render_to_string("quality/tables/items/processing_table.html")
    ret = {
        "html": html
    }
    return ret

@dajaxice_register
def updateProcessingReport(request, id_work_order, inspect_report_form):
    """
    author:mxl
    summary:
    update processing inspect report
    """
    try:
        inspect_report_form = InspectReportForm(deserialize_form(inspect_item_form), \
                                               instance=InspectReport.objects.get(base__work_order__id=id_work_order))
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
    "unqality": UnQualityGoodsBill,
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
                process_detail = ProcessDetail.objects.get(id=pid)
                materiel = Materiel.objects.get(id=process_detail.sub_materiel_belong.materiel_belong)
                bill = bill_model.get_or_create(process_detail=process_detail)
                bill.texture= materiel.material
                bill.weight=materiel.total_weight
                bill.schematic_index=materiel.schematic_index
                bill.processname=process_detail.processname.name
                bill.name=materiel.name
                bill.total_count += 1
                if bill_type == "repair":
                    bill.repair_count += 1
                elif bill_type == "unqality":
                    bill.unquality_count =+ 1
                elif bill_type == "scrap":
                    bill.scrap_count += 1
                bill.save()
                
                process_inspect_item = process_detail.processinspectitem
                process_inspect_item.add_to_unpass = True
                process_inspect_item.save()

                success_ids.append(pid)
            except:
                pass
    ret = {
        "success_ids": success_ids,
        "cate": bill_type
    }
    return ret

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
    materiels = sub_work_order.order.materiel_set()
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
    category = Category.objects.get(name="IPROCESS") 
    inspect_report = InspectReport.objects.get_or_create(
        work_order=sub_order.order,
        category=category
    )
    feeding_report = FeedingReport.objects.get_or_create(
        base=inspect_report,
        sub_work_order=sub_order,
        product_name=sub_order.order.product_name
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
        "sub_work_order": sub_work_order,
        "items": items
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
def updateFeedingReport(request, id_work_order, inspect_report_form, feeding_report_form):
    """
    author:mxl
    summary:
    update feeding inspect report
    """
    try:
        inspect_report_form = InspectReportForm(deserialize_form(inspect_item_form), \
                                               instance=InspectReport.objects.get(base__work_order__id=id_work_order))
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
