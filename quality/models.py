from django.db import models

from const.models import WorkOrder
from django.contrib.auth.models import User

from const import *

# Create your models here.
class InspectCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'检验类别')

    class Meta:
        verbose_name = u'检验类别'
        verbose_name_plural = u'检验类别'

    def __unicode__(self):
        return "%s" % self.name

class InspectReport(models.Model):
    work_order = models.ForeignKey(WorkOrder,blank=False, null=False, verbose_name=u'检验报告')
    category = models.ForeignKey(InspectCategory, blank=False, null=False, verbose_name=u'检验类别')
    owner = models.ForeignKey(User, blank=True, null=True, verbose_name=u'责任人')
    checkdate = models.DateField(blank=True, null=True, verbose_name=u'审核日期')
    checkstatus = models.IntegerField(choices=QA_STATUS, blank=True, null=True, verbose_name=u'检验状态')
    conclusion = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'检验结论')
    extra = models.TextField(max_length=5000, blank=True, null=True, verbose_name=u"额外字段")

    class Meta:
        verbose_name=u'检验报告单'
        verbose_name_plural=u'检验报告单'

    def __unicode__(self):
        return "%s%s" % (self.category, self.work_order)

class InspectItem(models.Model):
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
        return "%s%s" % (self.report, self.index)

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
        return "%s" % self.base

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
        return "%s" % self.base

class ProcessInspectItem(models.Model):
    base = models.OneToOneField(InspectItem, verbose_name=u'报告项Base')
    process_index = models.IntegerField(verbose_name=u'工序序号')
    process_code = models.CharField(max_length=20, verbose_name=u'工序代号')

    class Meta:
        verbose_name=u'工序检验项'
        verbose_name_plural=u'工序检验项'

    def __unicode__(self):
        return "%s" % self.base

class FeedingReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告单Base')
    schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品图号")
    product_name = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品名称")
    container_cate = models.CharField(blan=True, null=True, max_length=50, verbose_name=u"容器类别")

    class Meta:
        verbose_name=u"零件投料报告"
        verbose_name_plural=u"零件投料报告"

    def __unicode__(self):
        return "%s" % self.base

class FeedingInspectItem(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
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
        return "%s" % base

class BarrelReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    container_cate = models.CharField(blan=True, null=True, max_length=50, verbose_name=u"容器类别")
    part_name = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"零件名称")
    product_name = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品名称")
    texture = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"材质")
    product_name = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品名称")
    specification = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"规格")

    class Meta:
        verbose_name=u"封头/筒体检验"
        verbose_name_plural=u"封头/筒体检验"

    def __unicode__(self):
        return "%s" % self.base

class BarrelInspectItem(models.Model):
    process_index = models.CharField(max_length = 50, verbose_name = u"工序")
    check_item = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"检验项目")
    stipulate = models.FloatField(blank = True, null = True, verbose_name = u"规定值")
    real = models.FloatField(blank = True, null = True, verbose_name = u"实际值")
    operator = models.ForeignKey(User, verbose_name = u"操纵者")
    
    class Meta:
        verbose_name=u"封头/筒体检验项"
        verbose_name_plural=u"封头/筒体检验项"

    def __unicode__(self):
        return "%s" % self.base

class AssembleReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品图号")
    container_cate = models.CharField(blan=True, null=True, max_length=50, verbose_name=u"容器类别")

    class Meta:
        verbose_name=u"装配检验报告"
        verbose_name_plural=u"装配检验报告"

    def __unicode__(self):
        return "%s" % base

class AssembleInspectItem(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    check_item = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"检验项目")
    stipulate = models.FloatField(blank = True, null = True, verbose_name = u"规定值")
    real = models.FloatField(blank = True, null = True, verbose_name = u"实际值")

    class Meta:
        verbose_name=u"装配检验项"
        verbose_name_plural=u"装配检验项"

    def __unicode__(self):
        return "%s" % self.base

class PressureReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    product_no = models.CharField(max_length=20, verbose_name=u"产品编号")
    position = models.CharField(max_length=50, verbose_name=u"试压部位")
    techcard_no = models.CharField(max_length=50, verbose_name=u"工艺卡编号")
    media = models.CharField(max_length=50, verbose_name=u"试压介质")
    stipulate_media = models.FloatField(verbose_name=u"要求介质温度")
    real_media = models.FloatField(verbose_name=u"实际介质温度")
    stipulate_env_ = models.FloatField(verbose_name=u"要求环境温度")
    real_env_ = models.FloatField(verbose_name=u"实际环境温度")
    stipulate_curve = models.FileField(null=True, blank=True, upload_to=settings.QUALITY_FILE_PATH + "/%Y/%m/%d", verbose_name=u"要求压力试验曲线")
    real_curve = models.FileField(null=True, blank=True, upload_to=settings.QUALITY_FILE_PATH + "/%Y/%m/%d", verbose_name=u"实际压力试验曲线")

    class Meta:
        verbose_name=u"压力试验报告"
        verbose_name_plural=u"压力试验报告"

    def __unicode__(self):
        return "%s" % base

class PressureInspectItem(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    no = models.CharField(max_length=20, verbose_name=u"编号")
    range = models.FloatField(verbose_name=u"量程")
    diameter = models.FloatField(verbose_name=u"表盘直径")
    precision_level = models.CharField(max_length=20, verbose_name=u"精度等级")
    number = models.FloatField(max_length=20, verbose_name=u"读数")

    class Meta:
        verbose_name=u"压力试验项"
        verbose_name_plural=u"压力试验项"

    def __unicode__(self):
        return "%s" % self.base

class FacadeReport(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告单Base')
    product_name = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"产品名称")
    product_no = models.CharField(max_length=20, verbose_name=u"产品编号")
    
    class Meta:
        verbose_name=u"外观检验"
        verbose_name_plural=u"外观检验"

    def __unicode__(self):
        return "%s" % self.base

class FacadeInspectItem(models.Model):
    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
    check_item = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"检验项目")
    stipulate = models.FloatField(blank = True, null = True, verbose_name = u"规定值")
    real = models.FloatField(blank = True, null = True, verbose_name = u"实际值")

    class Meta:
        verbose_name=u"外观检验项"
        verbose_name_plural=u"外观检验项"

    def __unicode__(self):
        return "%s" % self.base

#class HeatTreatmentReport(models.Model):
#    base = models.OneToOneField(InspectReport, verbose_name=u'报告单Base')
#    product_no = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"产品编号")
#    position = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"部位")
#    schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"部件图号")
#    treat_method = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"热处理方式")
#
#    class Meta:
#        verbose_name=u"热处理检验"
#        verbose_name_plural=u"热处理检验"
#
#    def __unicode__(self):
#        return "%s" % self.base
#
#class HeatTreatmentInspectItem(models.Model):
#    base = models.OneToOneField(InspectReport, verbose_name=u'报告项Base')
#
#
#    class Meta:
#        verbose_name=u"热处理检验项"
#        verbose_name_plural=u"热处理检验项"
#
#    def __unicode__(self):
#        return "%s" % self.base


class FinalInspect(models.Model):
    work_order = models.ForeignKey(WorkOrder, verbose_name=u"所属工作令")
    status = models.IntegerField(default=0, verbose_name=u"检验状态")
    review = models.IntegerField(choices=REVIEW_COMMENTS_CHOICES, verbose_name=u"审核")

    class Meta:
        verbose_name=u"最终审核"
        verbose_name_plural=u"最终审核"

    def __unicode__(self):
        return "%s" % self.work_order

class UnQuilityGoods(models.Model):
    work_order = models.ForeignKey(WorkOrder, verbose_name=u"所属工作令")
    weight = models.FloatField(blank=True, null=True, verbose_name=u"单重")
    total_count = models.IntegerField(blank=True, null=True, verbose_name=u"交检数")
    no = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"本单号")
    schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"图号")
    process_index = models.CharField(max_length = 50, blank=True, null=True, verbose_name = u"工序")
    unquality_count = models.IntegerField(blank=True, null=True, verbose_name=u"不合格数")
    operator = models.ForeignKey(User, verbose_name=u"操作者")
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"名称")
    texture = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"材质")

    reason = models.TextField(max_length=1000, null=True, blank=True, verbose_name=u"不合格情况及原因")
    tech_opinion = models.TextField(max_length=1000, null=True, blank=True, verbose_name=u"工艺科意见")
    design_opinion = models.TextField(max_length=1000, null=True, blank=True, verbose_name=u"设计所意见")
    manager_opinion = models.TextField(max_length=1000, null=True, blank=True, verbose_name=u"技术负责人意见")

    class Meta:
        verbose_name=u"不合格品处理单"
        verbose_name_plural=u"不合格品处理单"

    def __unicode__(self):
        return "%s" % self.work_order
