# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from purchasing.models import BidForm,ArrivalInspection,Supplier,PurchasingEntry,PurchasingEntryItems
from const import *
from const.models import Materiel
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.models import User
from django.db import transaction 
from const.models import WorkOrder
from const.forms import InventoryTypeForm
from purchasing.forms import SupplierForm

@dajaxice_register
def searchPurchasingFollowing(request,bidid):
    bidform_processing=BidForm.objects.filter(bid_id=bidid)
    context={
        "bidform":bidform_processing,
        "BIDFORM_STATUS_SELECT_SUPPLIER":BIDFORM_STATUS_SELECT_SUPPLIER,
        "BIDFORM_STATUS_INVITE_BID":BIDFORM_STATUS_INVITE_BID,
        "BIDFORM_STATUS_PROCESS_FOLLOW":BIDFORM_STATUS_PROCESS_FOLLOW,
        "BIDFORM_STATUS_CHECK_STORE":BIDFORM_STATUS_CHECK_STORE 
    }
    purchasing_html=render_to_string("purchasing/purchasingfollowing/purchasing_following_table.html",context)
    data={
        'html':purchasing_html
    }
    return simplejson.dumps(data)

@dajaxice_register
def checkArrival(request,aid,cid):
    arrivalfield = ARRIVAL_CHECK_FIELDS[cid]
    cargo_obj = ArrivalInspection.objects.get(id = aid)
    val = not getattr(cargo_obj,arrivalfield)
    setattr(cargo_obj,arrivalfield,val)
    cargo_obj.save()
    val = getattr(cargo_obj,arrivalfield)
    data = {
        "flag":val, 
    }
    return simplejson.dumps(data)

@dajaxice_register
@transaction.commit_manually
def genEntry(request,bid):
    try:
        bidform = BidForm.objects.get(bid_id = bid)
        user = request.user
        purchasingentry = PurchasingEntry(bidform = bidform,purchaser=user,inspector = user , keeper = user) 
        purchasingentry.save()
    except Exception, e:
        transaction.rollback()
        print e
    flag = isAllChecked(bid,purchasingentry)
    if flag:
        transaction.commit()
    else:
        transaction.rollback()
    data = {
        'flag':flag,
    }
    return simplejson.dumps(data)

@dajaxice_register
def SupplierUpdate(request,supplier_id):
    supplier=Supplier.objects.get(pk=supplier_id)

    supplier_html=render_to_string("purchasing/supplier/supplier_file_table.html",{"supplier":supplier})
    return simplejson.dumps({'supplier_html':supplier_html})

def isAllChecked(bid,purchasingentry):
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid)
    bidform = BidForm.objects.get(bid_id = bid)
    for cargo_obj in cargo_set:
        entryitem = PurchasingEntryItems(material = cargo_obj.material,bidform = bidform)
        for key,field in ARRIVAL_CHECK_FIELDS.items():
            val = getattr(cargo_obj,field)
            if not val:
                return False
        entryitem.save()
    return True

@dajaxice_register
def chooseInventorytype(request,pid):
    #pid=int(pid)
    temp=Materiel.objects.filter(inventory_type__id=pid)
    context={
        "inventory_detail_list":temp,
    }
    new_order_form_html = render_to_string("widgets/new_order_form.html",context)
    new_purchasing_form_html = render_to_string("widgets/new_purchasing_form.html",context)
    inventory_detail_html = render_to_string("widgets/inventory_detail_table.html",context)
    main_material_quota_html = render_to_string("widgets/main_material_quota.html",context)
    accessory_quota_html = render_to_string("widgets/accessory_quota.html",context)
    first_send_detail_html = render_to_string("widgets/first_send_detail.html",context)
    out_purchasing_detail_html = render_to_string("widgets/out_purchasing_detail.html",context)
    cast_detail_html = render_to_string("widgets/cast_detail.html",context)
    
    return simplejson.dumps({
        "new_order_form_html":new_order_form_html,
        "new_purchasing_form_html":new_purchasing_form_html,
        "inventory_detail_html":inventory_detail_html,
        "main_material_quota_html":main_material_quota_html,
        "accessory_quota_html":accessory_quota_html,
        "first_send_detail_html":first_send_detail_html,
        "out_purchasing_detail_html":out_purchasing_detail_html,
        "cast_detail_html":cast_detail_html
        })

@dajaxice_register
def pendingOrderSearch(request, order_index):
    """
    JunHU
    summary: ajax function to search the order set by order index
    params: order_index: the index of the work order
    return: table html string
    """
    inventoryTypeForm = InventoryTypeForm()
    orders = WorkOrder.objects.filter(order_index__startswith = order_index)
    context = {"inventoryTypeForm": inventoryTypeForm,
               "orders": orders
              }
    html = render_to_string("purchasing/pending_order/pending_order_table.html", context)
    return html

@dajaxice_register
def getInventoryTable(request, table_id, order_index):
    context = {}
    html = render_to_string("purchasing/inventory_table/main_materiel.html", context)
    return html


@dajaxice_register
def SupplierAddorChange(request,mod,supplier_form):
    if mod==-1:
        supplier_form=SupplierForm(deserialize_form(supplier_form))
        supplier_form.save()
    else:
        supplier=Supplier.objects.get(pk=mod)
        supplier_form=SupplierForm(deserialize_form(supplier_form),instance=supplier)
        supplier_form.save()
    table=refresh_supplier_table(request)
    print table
    ret={"status":'0',"message":u"供应商添加成功","table":table}
    return simplejson.dumps(ret)

def refresh_supplier_table(request):
    suppliers=Supplier.objects.all()
    context={
        "suppliers":suppliers,
    }
    return render_to_string("purchasing/supplier/supplier_table.html",context)
