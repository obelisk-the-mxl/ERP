#!/usr/bin/env python
# coding=utf-8

from django import forms

from models import InspectItem, MaterielInspectItem, InspectReport, MaterielReport

class InspectReportForm(forms.ModelForm):
    class Meta:
        model = InspectReport
        exclude = {"id", "category", "extra"}
        widgets = {
            "work_order": forms.TextInput(attrs={"class": "input-medium", "readonly": "readonly"}),
            "checkstatus": forms.Select(attrs={"class": "input-medium"}),
            "conclusion": forms.TextInput(attrs={"class": "input-medium"}),
        }

class InspectItemForm(forms.ModelForm):
    class Meta:
        model = InspectItem
        exclude = {"id", "checkuser", "checkdate"}
        widgets = {
            "index" : forms.TextInput(attrs = {"class" : "input-medium"}),
            "report" : forms.TextInput(attrs = {"class" : "input-medium"}),
            "checkstatus" : forms.Select(attrs = {"class" : "input-medium"}),
            "extra" : forms.TextInput(attrs = {"class" : "input-medium"}),
        }

class MaterielItemForm(forms.ModelForm):
    class Meta:
        model = MaterielInspectItem
        exclude = {"id", "base_item"}
        widgets = {
            "materiel_name" : forms.TextInput(attrs = {"class" : "input-medium"}),
            "specification" : forms.TextInput(attrs = {"class" : "input-medium"}),
            "dilivery_status" : forms.TextInput(attrs = {"class" : "input-medium"}),
            "amount" : forms.TextInput(attrs = {"class" : "input-medium"}),
            "standard" : forms.TextInput(attrs = {"class" : "input-medium"}),
            "certification" : forms.TextInput(attrs = {"class" : "input-medium"})
        }

class MaterielReportForm(forms.ModelForm):
    class Meta:
        model = MaterielReport
        exclude = {"id", "base"}
        widgets ={
            "contact_number": forms.TextInput(attrs={"class": "input-medium"}),
            "index": forms.TextInput(attrs={"class": "input-medium"}),
            "manufactory": forms.TextInput(attrs={"class": "input-medium"}),
            "sell": forms.TextInput(attrs={"class": "input-medium"}),
            "code_mark": forms.TextInput(attrs={"class": "input-medium"}),
            "type": forms.TextInput(attrs={"class": "input-medium"})
        }
