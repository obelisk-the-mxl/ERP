#!/usr/bin/env python
# coding=utf-8

from django import forms
from const.models import InventoryType

class InventoryTypeForm(forms.Form):
    """
    JunHU
    summary: store all type of source inventory list
    """
    TYPE_CHOICES = tuple((item.id, item) for item in InventoryType.objects.all())

    inventory_type = forms.ChoiceField(choices = TYPE_CHOICES, widget = forms.Select(attrs = {'class': 'form-control input'}))


