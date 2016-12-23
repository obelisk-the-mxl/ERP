#!/usr/bin/env python
# coding=utf-8

from const import CheckPass, CheckUnPass, IBARREL, IASSEMBLE, IPRESSURE, IFACADE
from quality.models import InspectItem, InspectReport, \
        BarrelReport, BarrelInspectItem, AssembleReport, AssembleInspectItem, \
        PressureReport, FacadeReport, FacadeInspectItem

def check_report_canbe_pass(report_id):
    if report.status != CheckPass:
        return True
    unpass_inspect_items = InspectItem.objects.filter(base_item__report__id=report_id).filter(status=CheckUnPass)
    if unpass_inspect_items:
        return False
    return True

def check_report_canbe_finish(report):
    not_mark = []
    if not report.checkuser:
        not_mark.append(u"报告单检验")
    inspect_items = report.inspectitem_set.all()
    for item in inspect_items:
        if not item.checkuser:
            not_mark.append(u"报告项检验")
            break
    marks = report.inspectmark_set_all()
    for mark in marks:
        if not mark.marker:
            not_mark.append(mark.title)
    return not_mark

models_dict = {
    IBARREL: {
        "report": BarrelReport,
        "item": BarrelInspectItem
    },
    IASSEMBLE: {
        "report": AssembleReport,
        "item": AssembleInspectItem
    },
    IPRESSURE: {
        "report": PressureReport,
    },
    IFACADE: {
        "report": FacadeReport,
        "item": FacadeInspectItem,
    }
}

def afterFinish(sub_work_order_id, category, create_item_func=None):
    cur_model_dict = models_dict.get(category)
    cur_report_model = cur_model_dict.get("report")
    next_model_dict = models_dict.get(category + 1, {})
    
    sub_work_order = SubWorkOrder.objects.get(id=sub_work_order_id).select_related("order")

    cur_report_finished = False
    if category == IBARREL:
        """
        barrel report
        """
        all_report = cur_report_model.objects.filter(sub_materiel__sub_order__id=sub_work_order_id)
        not_finished = filter(lambda x: x.base.is_finished==False, all_report)
        if not_finished:
            cur_report_finished = True
    else:
        report = cur_report_model.objects.get(sub_work_order__id=sub_work_order_id)
        cur_report_finished = report.is_finished

    if cur_report_finished:
        """
        all report of this sub work order is finished, generate next one
        """
        if next_model_dict:
            """
            if has next one
            """
            inspect_report = InspectReport.objects.create(
                work_order=sub_work_order.order,
                category=category
            )
            next_report_model = next_model_dict.get("report")
            report = next_report_model.objects.create(
                base=inspect_report,
                sub_work_order=sub_work_order
            )
            if create_item_func:
                create_item_func(report=report, category=category)

