#!/usr/bin/env python
# coding=utf-8

from django import forms
from const import INSPECT_CATEGORY_CHOICE
from quality.models import InspectItem, MaterielInspectItem, InspectReport, MaterielReport, \
        ProcessInspectItem, FeedingReport, FeedingInspectItem, BarrelReport, BarrelInspectItem, \
        InspectItemConst, AssembleReport, AssembleInspectItem, PressureReport

class InspectCategoryForm(forms.Form):
    categories = forms.ChoiceField(label=u"检验类别", widget=forms.Select(attrs={"class": "form-control input"}))

    def __init__(self, *args, **kwargs):
        super(InspectCategoryForm, self).__init__(*args, **kwargs)
        self.fields["categories"].choices = INSPECT_CATEGORY_CHOICE

class InspectItemConstForm(forms.ModelForm):
    class Meta:
        model = InspectItemConst
        exclude = {"id", "index", "category"}
        widgets = {
            "check_item": forms.TextInput(attrs={"class": "input-medium"}),
            "stipulate": forms.TextInput(attrs={"class": "input-medium"}),
        }

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
        widgets = {
            "contact_number": forms.TextInput(attrs={"class": "input-medium"}),
            "index": forms.TextInput(attrs={"class": "input-medium"}),
            "manufactory": forms.TextInput(attrs={"class": "input-medium"}),
            "sell": forms.TextInput(attrs={"class": "input-medium"}),
            "code_mark": forms.TextInput(attrs={"class": "input-medium"}),
            "type": forms.TextInput(attrs={"class": "input-medium"})
        }

class UnCheckBillForm(forms.Form):
    total_count = forms.IntegerField(label=u"交检数", required=True, widget=forms.TextInput(attrs={'class':'form-control span2', 'id':'total_count'}))

class UnQualityGoodsBillForm(forms.Form):
    unquality_count = forms.IntegerField(label=u"不合格数", required=True, widget=forms.TextInput(attrs={'class':'form-control span2', 'id':'unquality_count'}))
    

class RepairBillForm(forms.Form):
    repair_count = forms.IntegerField(label=u"返修数", required=True, widget=forms.TextInput(attrs={'class':'form-control span2', 'id':'repair_count'}))
    after_repair_check = forms.CharField(label=u"修后检查", required=True, widget=forms.TextInput(attrs={'class':'form-control span2', 'id':'after_repair_check'}))


class ScrapBillForm(forms.Form):
    scrap_count = forms.IntegerField(label=u"报废数", required=True, widget=forms.TextInput(attrs={'class':'form-control span2', 'id':'scrap_count'}))

class FeedingReportForm(forms.ModelForm):
    class Meta:
        model = FeedingReport
        exclude = {"id", "base", "product_name"}
        widgets = {
            "sub_work_order": forms.TextInput({"class": "input-medium", "readonly": "readonly"}),
            "product_name": forms.TextInput({"class": "input-medium", "readonly": "readonly"}),
            "schematic_index": forms.TextInput(attrs={"class": "input-medium"}),
            "container_type": forms.TextInput(attrs={"class": "input-medium"})
        }

class FeedingInspectItemForm(forms.ModelForm):
    class Meta:
        model = FeedingInspectItem
        exclude = {"id", "base_item"}
        widgets = {
            "part_schematic_index": forms.TextInput({"class": "input-medium", "readonly": "readonly"}),
            "part_name": forms.TextInput({"class": "input-medium", "readonly": "readonly"}),
            "draw_texture": forms.TextInput({"class": "input-medium", "readonly": "readonly"}),
            "draw_specification": forms.TextInput({"class": "input-medium", "readonly": "readonly"}),
            "real_texture": forms.TextInput({"class": "input-medium"}),
            "real_specification": forms.TextInput({"class": "input-medium"}),
            "replace_code": forms.TextInput({"class": "input-medium"}),
            "texture_mark": forms.TextInput({"class": "input-medium"}),
            "amount": forms.TextInput({"class": "input-medium"}),
        }

class BarrelReportForm(forms.ModelForm):
    class Meta:
        model = BarrelReport
        exclude = {"id", "sub_materiel"}
        widgets = {
            "container_type": forms.TextInput({"class": "input-medium"})
        }

class BarrelInspectItemForm(forms.ModelForm):
    class Meta:
        model = BarrelInspectItem
        include = {"real"}
        widgets = {
            "real": forms.TextInput({"class": "input-medium"})
        }

class AssembleReportForm(forms.ModelForm):
    class Meta:
        model = AssembleReport
        include = {"container_type"}
        widgets = {
            "container_type": forms.TextInput({"class": "input-medium"})
        }

class AssembleInspectItemForm(forms.ModelForm):
    class Meta:
        model = AssembleReport
        include = {"real"}
        widgets = {
            "real": forms.TextInput({"class": "input-medium"})
        }

class PressureReportForm(forms.ModelForm):
    class Meta:
        model = PressureReport
        exclude = {"id", "base"}
        widgets = {
            "product_no": forms.TextInput({"class": "input-medium"}),
            "position": forms.TextInput({"class": "input-medium"}),
            "techcard_no": forms.TextInput({"class": "input-medium"})
        }

