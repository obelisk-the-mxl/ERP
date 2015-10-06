# coding: UTF-8
from django.shortcuts import render
from purchasing.models import BidForm,ArrivalInspection,Supplier
from const import *
from const.forms import InventoryTypeForm
from const.models import WorkOrder, InventoryType
from purchasing.forms import SupplierForm, BidApplyForm, QualityPriceCardForm

def purchasingFollowingViews(request):
    """
    chousan1989
    """
    bidform_processing=BidForm.objects.filter(bid_status__main_status__gte=BIDFORM_STATUS_SELECT_SUPPLIER,bid_status__main_status__lte=BIDFORM_STATUS_CHECK_STORE)

    context={
        "bidform":bidform_processing,
        "BIDFORM_STATUS_SELECT_SUPPLIER":BIDFORM_STATUS_SELECT_SUPPLIER,
        "BIDFORM_STATUS_INVITE_BID":BIDFORM_STATUS_INVITE_BID,
        "BIDFORM_STATUS_PROCESS_FOLLOW":BIDFORM_STATUS_PROCESS_FOLLOW,
        "BIDFORM_STATUS_CHECK_STORE":BIDFORM_STATUS_CHECK_STORE 
    }

    return render(request,"purchasing/purchasing_following.html",context)


def pendingOrderViews(request):
    """
    JunHU
    summary: view function of pendingorder page
    params: NULL
    return: NULL
    """
    return render(request, "purchasing/pending_order.html")

def selectSupplierViews(request):
    context={}
    return render(request,"purchasing/select_supplier.html",context)

def supplierManagementViews(request):
    suppliers=Supplier.objects.all()
    supplier_form=SupplierForm()
    context={
        "suppliers":suppliers,
        "supplier_form":supplier_form
    }
    return render(request,"purchasing/supplier/supplier_management.html",context)


def bidTrackingViews(request):
    """
    Liu Ye
    """
    qualityPriceCardForm = QualityPriceCardForm()
    bidApplyForm = BidApplyForm()

    bid_status = []
    bid_status.append({"name":u"招标申请表",         "class":"btn-success"})
    bid_status.append({"name":u"分公司领导批准",     "class":"btn-success"})
    bid_status.append({"name":u"滨海公司领导批准",   "class":""})
    bid_status.append({"name":u"滨海招标办领导批准", "class":"btn-danger"})
    bid_status.append({"name":u"中标通知书",         "class":""})
    context = {"bid_status": bid_status,
               "qualityPriceCardForm": qualityPriceCardForm,
               "bidApplyForm": bidApplyForm,
             }
    return render(request, "purchasing/bid_track.html", context)
def arrivalInspectionViews(request):
    bidFormSet = BidForm.objects.filter(bid_status__part_status = BIDFORM_PART_STATUS_CHECK) 
    
    context = {
        "bidFormSet":bidFormSet,
    }
    return render(request,"purchasing/purchasing_arrival.html",context)

def arrivalCheckViews(request,bid):
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid)
    context = {
        "cargo_set":cargo_set,
        "bid":bid,
    }
    return render(request,"purchasing/purchasing_arrivalcheck.html",context)

def inventoryTableViews(request):
    order_index = request.GET.get("order_index")
    tableid = request.GET.get("tableid")
    order = WorkOrder.objects.get(order_index = order_index)
    inventoryType = InventoryType.objects.get(id = tableid)
    context = {"order": order,
               "inventoryType": inventoryType,
    }
    return render(request, "purchasing/inventory_table_base.html", context)
