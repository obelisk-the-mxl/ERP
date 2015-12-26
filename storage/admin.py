#coding=UTF-8
from models import *

from django.contrib import admin

Registers = (
    WeldingMaterialApplyCard,
    StoreRoom,
    WeldingMaterialHumitureRecord,
    WeldingMaterialBakeRecord,
    SteelMaterialPurchasingEntry,
    SteelMaterial,
    BoardSteelMaterialLedger,
    BarSteelMaterialLedger,
    CommonSteelMaterialReturnCardInfo,
    CommonSteelMaterialApplyCardInfo,
    BoardSteelMaterialReturnCardContent,
    BoardSteelMaterialApplyCardContent,
    BarSteelMaterialReturnCardContent,
    BarSteelMaterialApplyCardContent,
    WeldRefund,
    AuxiliaryTool,
    AuxiliaryToolApplyCard,
    AuxiliaryToolEntryCard,
    AuxiliaryToolEntryCardList,
    WeldMaterialEntry,
    WeldMaterialEntryItems,
    WeldStoreList,
    WeldStoreThread,
    OutsideStandardEntry,
    OutsideStandardItem,
)

for reg in Registers:
    admin.site.register(reg)
