# coding: UTF-8

from uuid import uuid4

from django.db import models

from django.contrib.auth.models import User

from const import UnCheck, QA_STATUS, DILIVER_STATUS, UNDILIVER, \
        REVIEW_COMMENTS_CHOICES, QUALITY_MARK_DICT, INSPECT_CATEGORY_CHOICE, \
        UNPASS_TYPE
from const.models import WorkOrder, SubWorkOrder
from production.models import ProcessDetail, SubMateriel

import settings

# Create your models here.

class InspectReport(models.Model):
    id = models.CharField(max_length=40, default=uuid4, primary_key=True)
    work_order = models.ForeignKey(WorkOrder,blank=False, null=False, verbose_name=u'检验报告')
    category = models.IntegerField(choices=INSPECT_CATEGORY_CHOICE, blank=False, null=False, verbose_name=u'检验类别')
    checkuser = models.ForeignKey(User, blank=True, null=True, verbose_name=u'检查员')
    checkdate = models.DateField(blank=True, null=True, verbose_name=u'审核日期')
    checkstatus = models.IntegerField(choices=QA_STATUS, blank=True, null=True, verbose_name=u'检验状态')
    conclusion = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'检验结论')
    extra = models.TextField(max_length=5000, blank=True, null=True, verbose_name=u"额外字段")
    is_finished = models.BooleanField(default=False, verbose_name=u"是否完成检验")

    class Meta:
        verbose_name=u'检验报告单'
        verbose_name_plural=u'检验报告单'

    def __unicode__(self):
        return u"%s%s" % (self.category, self.work_order)

    def save(self, *args, **kwargs):
        super(InspectReport, self).save(*args, **kwargs)
        mark_list = QUALITY_MARK_DICT.get(self.category, [])
        for mark in mark_list:
            inspect_report_mark = InspectReportMark(
                report=self,
                title=mark
            )
            inspect_report_mark.save()

class InspectItem(models.Model):
    id = models.CharField(max_length=40, default=uuid4, primary_key=True)
    index = models.IntegerField(blank=False, null=False, verbose_name=u'检验序号')
    report = models.ForeignKey(InspectReport, blank=False, null=False, verbose_name=u'检验报告单')
    checkdate = models.DateField(blank=True, null=True, verbose_name=u'检验日期')
    checkstatus = models.IntegerField(choices=QA_STATUS, blank=False, null=False, default=UnCheck, verbose_name=u'检验状态')
    checkuser = models.ForeignKey(User, blank=True, null=True, verbose_name=u'检验者')
    extra = models.TextField(max_length=5000, blank=True, null=True, verbose_name=u"额外字段")

    class Meta:
        verbose_name=u'检验项'
        verbose_name_plural = u'检验项'

    def __unicode__(self):
        return u"%s%s" % (self.report, self.index)

class InspectReportMark(models.Model):
    report = models.ForeignKey(InspectReport, blank=False, null=False, verbose_name=u'检验报告单')
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name=u"签字标题")
    marker = models.ForeignKey(User, blank=True, null=True, verbose_name=u"签字人")
    markdate = models.DateField(blank=True, null=True, verbose_name=u"签字日期")

    class Meta:
        verbose_name=u"报告单签字"
        verbose_name_plural=u"报告单签字"

    def __unicode__(self):
        return "%s-%s" % (self.report, self.title)

class MaterielReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告单Base')
    contact_number = models.IntegerField(blank=False, null=False, verbose_name=u'订货合同编号')
    index = models.CharField(max_length=20, verbose_name=u'编号')
    manufactory = models.CharField(max_length=100, verbose_name=u'制造厂')
    sell = models.CharField(max_length=100, verbose_name=u'经销厂')
    code_mark = models.CharField(max_length=100, verbose_name=u'编码标记')
    type = models.CharField(max_length=50, verbose_name=u"检验单类型")

    class Meta:
        verbose_name=u'材料检验报告'
        verbose_name_plural=u'材料检验报告'

    def __unicode__(self):
        return u"%s" % self.base

class MaterielInspectItem(models.Model):
    base_item = models.OneToOneField(InspectItem, verbose_name=u'检验项Base')
    materiel_name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'材料名称')
    specification = models.CharField(max_length=50, verbose_name=u'材料规格')
    dilivery_status = models.IntegerField(default=UNDILIVER, choices=DILIVER_STATUS, verbose_name=u'交货状态')
    amount = models.IntegerField(default=0, verbose_name=u'数量')
    standard = models.CharField(max_length=100, verbose_name=u'产品标准')
    certification = models.CharField(max_length=100, verbose_name=u'材料质量证明书号')

    class Meta:
        verbose_name=u'材料检验项'
        verbose_name_plural=u'材料检验项'

    def __unicode__(self):
        return u"%s" % self.base_item
    
class ProcessReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u"报告单")
    sub_work_order = models.OneToOneField(SubWorkOrder, verbose_name=u"子工作令")

    class Meta:
        verbose_name=u"工序检验报告单"
        verbose_name_plural=u"工序检验报告单"

    def __unicode__(self):
        return u"%s" % self.base

class ProcessInspectItem(models.Model):
    base_item = models.OneToOneField(InspectItem, verbose_name=u'报告项Base')
    #process_index = models.IntegerField(verbose_name=u'工序序号')
    #process_code = models.CharField(max_length=20, verbose_name=u'工序代号')
    process_detail = models.OneToOneField(ProcessDetail, verbose_name=u"工序详细")
    add_to_unpass = models.BooleanField(default=False, verbose_name=u"是否加入未通过")

    class Meta:
        verbose_name=u'工序检验项'
        verbose_name_plural=u'工序检验项'

    def __unicode__(self):
        return u"%s" % self.base_item

class FeedingReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告单Base')
    sub_work_order = models.OneToOneField(SubWorkOrder, verbose_name=u"子工作令")
    schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品图号")
    product_name = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品名称")
    container_type = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"容器类别")

    class Meta:
        verbose_name=u"零件投料报告"
        verbose_name_plural=u"零件投料报告"

    def __unicode__(self):
        return u"%s" % self.base

class FeedingInspectItem(models.Model):
    base_item = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    part_schematic_index = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"零件图号")
    part_name = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"零件名称")
    draw_texture = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"图纸材质")
    draw_specification = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"图纸规格")
    real_texture = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"实际材质")
    real_specification = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"实际规格")
    replace_code = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"代用单号")
    texture_mark = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"材质标记")
    amount = models.IntegerField(default=0, verbose_name=u'件数')
    remark = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"备注")
    
    class Meta:
        verbose_name=u"零件投料项"
        verbose_name_plural=u"零件投料项"

    def __unicode__(self):
        return u"%s" % base_item

class BarrelReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    sub_materiel = models.OneToOneField(SubMateriel, verbose_name=u"零件")
    container_cate = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"容器类别")
    #part_name = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"零件名称")
    #product_name = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品名称")
    #texture = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"材质")
    #product_name = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品名称")
    #specification = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"规格")

    class Meta:
        verbose_name=u"封头/筒体检验"
        verbose_name_plural=u"封头/筒体检验"

    def __unicode__(self):
        return u"%s" % self.base

class BarrelInspectItem(models.Model):
    base_item = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    process_detail = models.ForeignKey(ProcessDetail, verbose_name=u"工序")
    check_item = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"检验项目")
    stipulate = models.CharField(max_length=100, blank = True, null = True, verbose_name = u"规定值")
    real = models.CharField(max_length=100, blank = True, null = True, verbose_name = u"实际值")
    operator = models.ForeignKey(User, verbose_name = u"操纵者")
    
    class Meta:
        verbose_name=u"封头/筒体检验项"
        verbose_name_plural=u"封头/筒体检验项"

    def __unicode__(self):
        return u"%s" % self.base_item

class AssembleReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    sub_work_order = models.OneToOneField(SubWorkOrder, verbose_name=u"子工作令")
    #schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品图号")
    container_cate = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"容器类别")

    class Meta:
        verbose_name=u"装配检验报告"
        verbose_name_plural=u"装配检验报告"

    def __unicode__(self):
        return u"%s" % base

class AssembleInspectItem(models.Model):
    base_item = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    check_item = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"检验项目")
    stipulate = models.FloatField(blank = True, null = True, verbose_name = u"规定值")
    real = models.FloatField(blank = True, null = True, verbose_name = u"实际值")

    class Meta:
        verbose_name=u"装配检验项"
        verbose_name_plural=u"装配检验项"

    def __unicode__(self):
        return u"%s" % self.base

class PressureReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    sub_work_order = models.OneToOneField(SubWorkOrder, verbose_name=u"子工作令")
    product_no = models.CharField(max_length=20, verbose_name=u"产品编号")
    position = models.CharField(max_length=50, verbose_name=u"试压部位")
    techcard_no = models.CharField(max_length=50, verbose_name=u"工艺卡编号")

    class Meta:
        verbose_name=u"压力试验报告"
        verbose_name_plural=u"压力试验报告"

    def __unicode__(self):
        return u"%s" % base

class PressureReportItem(models.Model):
    index = models.IntegerField(blank=False, null=False, verbose_name=u'序号')
    text = models.CharField(max_length=100, verbose_name=u"文本")
    attr_name = models.CharField(max_length=20, verbose_name=u"属性")
    stipulate_value = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"值")

    class Meta:
        verbose_name=u"压力试验项"
        verbose_name_plural=u"压力试验项"

    def __unicode__(self):
        return u"%s" % self.text

class PressureReportValue(models.Model):
    report = models.ForeignKey(PressureReport, verbose_name=u"报告单")
    item = models.ForeignKey(PressureReportItem, verbose_name=u"项")
    value = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"值")

    class Meta:
        verbose_name=u"压力试验值项"
        verbose_name_plural=u"压力试验值项"

    def __unicode__(self):
        return "%s:%s" % (self.report, self.item)

class FacadeReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告单Base')
    sub_work_order = models.OneToOneField(SubWorkOrder, verbose_name=u"子工作令")
    product_name = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品名称")
    product_no = models.CharField(max_length=20, verbose_name=u"产品编号")
    
    class Meta:
        verbose_name=u"外观检验"
        verbose_name_plural=u"外观检验"

    def __unicode__(self):
        return u"%s" % self.base

class FacadeInspectItem(models.Model):
    base_item = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    check_item = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"检验项目")
    stipulate = models.FloatField(blank = True, null = True, verbose_name = u"规定值")
    real = models.FloatField(blank = True, null = True, verbose_name = u"实际值")

    class Meta:
        verbose_name=u"外观检验项"
        verbose_name_plural=u"外观检验项"

    def __unicode__(self):
        return u"%s" % self.base_item

class FinalInspect(models.Model):
    sub_work_order = models.ForeignKey(SubWorkOrder, verbose_name=u"所属子工作令")
    checkuser = models.ForeignKey(User, blank=True, null=True, verbose_name=u'检查员')
    checkdate = models.DateField(blank=True, null=True, verbose_name=u'审核日期')
    checkstatus = models.IntegerField(choices=QA_STATUS, blank=True, null=True, verbose_name=u'检验状态')

    class Meta:
        verbose_name=u"最终审核"
        verbose_name_plural=u"最终审核"

    def __unicode__(self):
        return u"%s" % self.work_order

class UnPassBill(models.Model):
    id = models.CharField(max_length=40, default=uuid4, primary_key=True)
    process_detail = models.ForeignKey(ProcessDetail, verbose_name=u"所属工序")
    #processname = models.CharField(max_length = 50, blank=True, null=True, verbose_name = u"工序")
    texture = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"材质")
    weight = models.FloatField(blank=True, null=True, verbose_name=u"单重")
    schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"图号")
    total_count = models.IntegerField(blank=True, null=True, verbose_name=u"交检数")
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"名称")
    operator = models.ForeignKey(User, verbose_name=u"操作者", related_name="operator")
    inspect_manager = models.ForeignKey(User, verbose_name=u"检查站长", related_name=u"inspect_manager")

    class Meta:
        verbose_name=u"不合格单"
        verbose_name_plural=u"不合格单"

    def __unicode__(self):
        return u"%s-%s" % (self.work_order, self.no)

class UnpassCounter(models.Model):
    work_order = models.ForeignKey(WorkOrder,blank=False, null=False, verbose_name=u'检验报告')
    cnt = models.IntegerField(default=0, verbose_name=u"计数")
    unpass_type = models.CharField(max_length=100, choices=UNPASS_TYPE, verbose_name=u"不合格类型")

    class Meta:
        verbose_name=u"不合格计数"
        verbose_name_plural=u"不合格计数"

    def __unicode__(self):
        return "%s %s" % (self.work_order, self.unpass_type)

class SignatureSheet(models.Model):
    bill = models.ForeignKey(UnPassBill, verbose_name=u"不合格单")
    text = models.CharField(max_length=50, verbose_name=u"签字文本")
    signer = models.ForeignKey(User, verbose_name=u"签字者")
    sign_date = models.DateField(verbose_name=u"日期")
    opinion = models.TextField(max_length=1000, null=True, blank=True, verbose_name=u"意见")
    
    class Meta:
        verbose_name=u"签字单"
        verbose_name_plural=u"签字单"

    def __unicode__(self):
        return u"%s:%s" % (self.bill, self.text)

class UnQualityGoodsBill(UnPassBill):
    reason = models.TextField(max_length=1000, null=True, blank=True, verbose_name=u"不合格情况及原因")
    inspect_marker = models.ForeignKey(User, null=True, blank=True, verbose_name=u"检验员", related_name="unquality_inspect_marker")
    inspect_manage_marker = models.ForeignKey(User, null=True, blank=True, verbose_name=u"检查站长", related_name="unquality_inspect_manage_marker")

    class Meta:
        verbose_name=u"不合格品处理单"
        verbose_name_plural=u"不合格品处理单"

    def __unicode__(self):
        return u"%s-%s" % (self.work_order)

class RepairBill(UnPassBill):
    reason = models.TextField(max_length=200, null=True, blank=True, verbose_name=u"退修原因")
    inspect_marker = models.ForeignKey(User, null=True, blank=True, verbose_name=u"检验员", related_name="repair_inspect_marker")
    inspect_manager_marker = models.ForeignKey(User, null=True, blank=True, verbose_name=u"检查站长", related_name="repair_inspect_manage_marker")
    repair_manage_marker = models.ForeignKey(User, null=True, blank=True, verbose_name=u"承修单位负责人", related_name="inspect_manage_marker")

    class Meta:
        verbose_name=u"退修单"
        verbose_name_plural=u"退休单"

    def __unicode__(self):
        return u"%s-%s" % (self.work_order)

class ScrapBill(UnPassBill):
    inspect_marker = models.ForeignKey(User, null=True, blank=True, verbose_name=u"检验员", related_name="scrap_inspect_marker")

    class Meta:
        verbose_name=u"报废单"
        verbose_name_plural=u"报废单"

    def __unicode__(self):
        return u"%s-%s" % (self.work_order)

class InspectItemConst(models.Model):
    category = models.IntegerField(choices=INSPECT_CATEGORY_CHOICE, blank=False, null=False, verbose_name=u'检验类别')
    index = models.IntegerField(blank=False, null=False, verbose_name=u'序号')
    check_item = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"检验项目")
    stipulate = models.CharField(max_length=100, blank = True, null = True, verbose_name = u"规定值")
     
    class Meta:
        verbose_name=u"检查项目常量"
        verbose_name_plural=u"检查项目常量"

    def __unicode__(self):
        return "%s-%s" % (self.category, self.check_item)

