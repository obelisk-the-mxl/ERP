#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-09-11 11:25
# Last modified: 2016-09-11 11:51
# Filename: forms.py
# Description:
#!/usr/bin/env python
# coding=utf-8

from django import forms
from const import *
from const.models import InventoryType, WorkOrder, SubWorkOrder
from users.models import Group

class WorkOrderForm(forms.Form):
    """
    JunHU
    summary: store all work orders
    """
    work_order = forms.ChoiceField(label=u"工作令", widget = forms.Select(attrs = {"class": "form-control input"}))
    def __init__(self, *args, **kwargs):
        super(WorkOrderForm, self).__init__(*args, **kwargs)
        WORKORDER_CHOICES = tuple((item.id, item) for item in WorkOrder.objects.all())
        self.fields["work_order"].choices = WORKORDER_CHOICES

class AuthorTypeForm(forms.Form):
    """
    JunHU
    summary: store all type of author type
    """
    _choices = map(lambda x: (x.cate, x.name), Group.objects.all())
    auth_type = forms.ChoiceField(choices = _choices, widget = forms.Select(attrs = {'class': 'form-control input'}))

class InventoryTypeForm(forms.Form):
    """
    JunHU
    summary: store all type of source inventory list
    """
    TYPE_CHOICES = tuple((item.name, item) for item in InventoryType.objects.all())

    inventory_type = forms.ChoiceField(choices = TYPE_CHOICES, widget = forms.Select(attrs = {'class': 'form-control input'}))


    def __init__(self, *args, **kwargs):
        super(InventoryTypeForm, self).__init__(*args, **kwargs)
        TYPE_CHOICES = tuple((item.name, item) for item in InventoryType.objects.all())
        self.fields["inventory_type"].choices = TYPE_CHOICES


class SubWorkOrderForm(forms.Form):
    """
    Author:mxl
    summary:
    store all sub work orders of a work order
    """
    sub_work_order = forms.ChoiceField(label=u"子工作令", widget = forms.Select(attrs = {"class": "form-control input"}))
    def __init__(self, *args, **kwargs):
        super(SubWorkOrderForm, self).__init__(*args, **kwargs)
        order_id = kwargs.get("order_id", 0)
        if order_id:
            kwargs.pop("order_id")
        else:
            orders = WorkOrder.objects.all()
            if orders:
                order = orders[0]
                order_id = order.id
        if order_id:
            CHOICES = tuple((item.id, "%s-%s" % (item.order, item.index)) for item in SubWorkOrder.objects.filter(order__id=order_id))
            self.fields["sub_work_order"].choices = CHOICES

