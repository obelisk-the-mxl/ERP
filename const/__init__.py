# coding: UTF-8

BIDFORM_STATUS_CREATE=10
BIDFORM_STATUS_SELECT_SUPPLIER=20
BIDFORM_STATUS_INVITE_BID=30
BIDFORM_STATUS_PROCESS_FOLLOW=40
BIDFORM_STATUS_CHECK_STORE=50
BIDFORM_STATUS_COMPLETE=60
BIDFORM_STATUS_STOP=-1

BIDFORM_PART_STATUS_CREATE=10
#BIDFORM_PART_STATUS_ESTABLISHMENT=20
#BIDFORM_PART_STATUS_APPROVED=30
BIDFORM_PART_STATUS_SELECT_SUPPLLER_APPROVED=40
BIDFORM_PART_STATUS_INVITE_BID_APPLY_SELECT=50
BIDFORM_PART_STATUS_INVITE_BID_FILL=55
BIDFORM_PART_STATUS_INVITE_BID_CARRY=95
BIDFORM_PART_STATUS_INVITE_BID_COMPLETE=97
BIDFORM_PART_STATUS_PROCESS_FOLLOW=100
BIDFORM_PART_STATUS_CHECK=110
BIDFORM_PART_STATUS_STORE=120
BIDFORM_PART_STATUS_COMPLETE=130
BIDFORM_PART_STATUS_STOP=-1

BIDFORM_STATUS_CHOICES=(

    (BIDFORM_STATUS_CREATE,u"标单生成"),
    (BIDFORM_STATUS_SELECT_SUPPLIER,u"供应商选择"),
    (BIDFORM_STATUS_INVITE_BID,u"招标"),
    (BIDFORM_STATUS_PROCESS_FOLLOW,u"过程跟踪"),
    (BIDFORM_STATUS_CHECK_STORE,u"检查入库"),
    (BIDFORM_STATUS_COMPLETE,u"标单完成"),
    (BIDFORM_STATUS_STOP,u"标单终止")
    
)

BIDFORM_PART_STATUS_CHOICES=(
    
    (BIDFORM_PART_STATUS_CREATE,u"标单创建"),
#   (BIDFORM_PART_STATUS_ESTABLISHMENT,u"标单编制"),
#   (BIDFORM_PART_STATUS_APPROVED,u"标单审批"),
    (BIDFORM_PART_STATUS_SELECT_SUPPLLER_APPROVED,u"供应商选择"),
    (BIDFORM_PART_STATUS_INVITE_BID_APPLY_SELECT,u"招标申请选择"),
    (BIDFORM_PART_STATUS_INVITE_BID_FILL,u"招标申请填写"),
    (BIDFORM_PART_STATUS_INVITE_BID_CARRY,u"招标中"),
    (BIDFORM_PART_STATUS_INVITE_BID_COMPLETE,u"中标确认"),
    (BIDFORM_PART_STATUS_PROCESS_FOLLOW,u"进程跟踪"),
    (BIDFORM_PART_STATUS_CHECK,u"标单检验"),
    (BIDFORM_PART_STATUS_STORE,u"标单入库"),
    (BIDFORM_PART_STATUS_COMPLETE,u"标单完成"),
    (BIDFORM_PART_STATUS_STOP,u"标单终止")
)
BIDFORM_PART_STATUS_DICT={
    "BIDFORM_PART_STATUS_INVITE_BID_APPLY_SELECT":BIDFORM_PART_STATUS_INVITE_BID_APPLY_SELECT,
    "BIDFORM_PART_STATUS_INVITE_BID_FILL":BIDFORM_PART_STATUS_INVITE_BID_FILL,
    "BIDFORM_PART_STATUS_INVITE_BID_CARRY":BIDFORM_PART_STATUS_INVITE_BID_CARRY,
    "BIDFORM_PART_STATUS_INVITE_BID_COMPLETE":BIDFORM_PART_STATUS_INVITE_BID_COMPLETE
    
}

APPROVED_PASS=0
APPROVED_NOT_PASS=1
APPROVED_RESULT_CHOICES=(
    (APPROVED_PASS,u"通过"),
    (APPROVED_NOT_PASS,u"不通过")
)
IDENTITYERROR = "登录帐号或密码有错误！"

ORDERFORN_STATUS_BEGIN = 0
ORDERFORN_STATUS_ESTABLISHMENT = 1
ORDERFORN_STATUS_AUDIT = 2
ORDERFORN_STATUS_APPROVED = 3
ORDERFORN_STATUS_FINISH= 4

ORDERFORM_STATUS_CHOICES = (
    (ORDERFORN_STATUS_BEGIN, u"创建中订购单"),
    (ORDERFORN_STATUS_ESTABLISHMENT, u"创建完成订购单"),
    (ORDERFORN_STATUS_AUDIT,u"审核通过订购单"),
    (ORDERFORN_STATUS_APPROVED,u"批准通过订购单"),
    (ORDERFORN_STATUS_FINISH, u"已终止历史订购单"),
)

RECHECK_CHOICE = (
    (True,u"是"),
    (False,u"否"),
)

MAIN_MATERIEL = "main_materiel"
AUXILIARY_MATERIEL = "auxiliary_materiel"
FIRST_FEEDING = "first_feeding"
OUT_PURCHASED = "out_purchased"
WELD_MATERIAL = "weld_material"
COOPERANT = "cooperant"

INVENTORY_TYPE = (
    (MAIN_MATERIEL, u"主材定额"),
    (AUXILIARY_MATERIEL, u"辅材定额"),
    (FIRST_FEEDING, u"先投件明细"),
    (OUT_PURCHASED, u"外购件明细"),
    (WELD_MATERIAL, u"焊材定额"),
    (COOPERANT, u"工序性外协明细")
)

SELL_TYPE = (
    (0, u"内销"),
    (1, u"外销"),
)

IMPLEMENT_CLASS_CHOICES = (
    (0, u"招标"),
    (1, u"议标"),
)

SEX_CHOICES = (
    (0, u"男"),
    (1, u"女"),
)
INDEX_LIST = tuple(
    (i, str(i)) for i in xrange(1, 11)
)

ARRIVAL_CHECK_FIELDS = {"mat":"material_confirm","sof":"soft_confirm","ins":"inspect_confirm"}

REVIEW_COMMENTS_CHOICE_WAIT = -1

REVIEW_COMMENTS_CHOICES = (
    (-1,u"未审核"),
    (0,u"通过"),
    (1,u"不通过"),
)
MAIN_MATERIEL = "main_materiel"
SUPPORT_MATERIEL = AUXILIARY_MATERIEL
MATERIEL_CHOICE = (
    (MAIN_MATERIEL, u"主材"),
    (SUPPORT_MATERIEL, u"辅材"),
)

ENTRYTYPE_WELD = 0
ENTRYTYPE_NORMTEILE = 1
ENTRYTYPE_ASSISTTOOL = 2
ENTRYTYPE_FORGING = 4

ENTRYTYPE_CHOICES = (
    (ENTRYTYPE_WELD,u"焊材"),
    (ENTRYTYPE_FORGING,u"锻件"),
    (ENTRYTYPE_NORMTEILE,u"标准件"),
    (ENTRYTYPE_ASSISTTOOL,u"辅助工具"),
)


ENTRYTYPE_BOARD = 0
ENTRYTYPE_BAR = 1

ENTRYTYPE_CHOICES_2 = (
    (ENTRYTYPE_BOARD,u"板材"),
    (ENTRYTYPE_BAR,u"型材"),
)

COOPERATION_OUTSIDEBUY = 0
STANDARD_OUTSIDEBUY = 1
FORGING_OUTSIDEBUY = 2
OUTSIDEBUY_TYPE = (
    (COOPERATION_OUTSIDEBUY,u"外协加工"),
    (STANDARD_OUTSIDEBUY,u"标准件"),
    (FORGING_OUTSIDEBUY,u"锻件"),
)

BOARD_STEEL = 0
BAR_STEEL = 1
STEEL_TYPE = (
    (BOARD_STEEL,u'板材'),
    (BAR_STEEL,u'型材'),
)

STOREROOM_CHOICES_WELD = 0
STOREROOM_CHOICES_STEEL = 1
STOREROOM_CHOICES_AUXILIARY_TOOL =2
STOREROOM_CHOICES_OUTSIDEBUY =3

STOREROOM_CHOICES=(
    (STOREROOM_CHOICES_WELD,u'焊材'),
    (STOREROOM_CHOICES_STEEL,u'钢材'),
    (STOREROOM_CHOICES_AUXILIARY_TOOL,u'辅助工具'),
    (STOREROOM_CHOICES_OUTSIDEBUY,u'外购件'),
)

KILOGRAM = 0
TON = 1
WEIGHT_MANAGEMENT=(
    (KILOGRAM,u'千克'),
    (TON,u'顿'),
)

SQUARE_METER = 0

AREA_MANAGEMENT=(
    (SQUARE_METER,u'平方米'),
)

METER = 0
CENTIMETER =1

LENGHT_MANAGEMENT=(
    (METER,u'米'),
    (CENTIMETER,u"厘米"),
)









PAGE_ELEMENTS = 10



NEWS_CATEGORY_COMPANYNEWS = "companynews"
NEWS_CATEGORY_IMPORTINFO = "importinfo"
NEWS_CATEGORY_DOCUMENTS = "documents"

NEW_CATEGORY_CHOICES = (
    (NEWS_CATEGORY_COMPANYNEWS, u"公司新闻"),
    (NEWS_CATEGORY_IMPORTINFO, u"重要通知"),
)

NEWS_MAX_LENGTH = 10000000
#-------------库存管理----------------#
STORAGE_CARD_STOP_STATUS = 10

ENTRYSTATUS_CHOICES_PUCAHSER = 0
ENTRYSTATUS_CHOICES_INSPECTOR = 1
ENTRYSTATUS_CHOICES_KEEPER = 2
ENTRYSTATUS_CHOICES_END = 3
ENTRYSTATUS_CHOICES_STOP = STORAGE_CARD_STOP_STATUS
ENTRYSTATUS_CHOICES = (
    (ENTRYSTATUS_CHOICES_PUCAHSER,u"待采购员确认"),
    (ENTRYSTATUS_CHOICES_INSPECTOR,u"待检查确认"),
    (ENTRYSTATUS_CHOICES_KEEPER,u"待库管确认"),
    (ENTRYSTATUS_CHOICES_END,u"入库完成"),
    (ENTRYSTATUS_CHOICES_STOP,u"入库终止"),
)

APPLYCARD_APPLICANT=0
APPLYCARD_AUDITOR=1
APPLYCARD_INSPECTOR=2
APPLYCARD_KEEPER=3
APPLYCARD_END = 4
APPLYCARD_STOP = STORAGE_CARD_STOP_STATUS
APPLYCARD_STATUS_CHOICES=(
        (APPLYCARD_APPLICANT,u'领用申请'),
        (APPLYCARD_AUDITOR,u'领用审核'),
        (APPLYCARD_INSPECTOR,u'领用检查'),
        (APPLYCARD_KEEPER,u'领用发料'),
        (APPLYCARD_END,u"领用完成"),
        (APPLYCARD_STOP,u"领用终止"),
        )

AUXILIARY_TOOL_APPLY_CARD_APPLICANT=0
AUXILIARY_TOOL_APPLY_CARD_AUDITOR=1
AUXILIARY_TOOL_APPLY_CARD_KEEPER=2
AUXILIARY_TOOL_APPLY_CARD_END=3
AUXILIARY_TOOL_APPLY_CARD_STOP = STORAGE_CARD_STOP_STATUS
AUXILIARY_TOOL_APPLY_CARD_STATUS=(
        (AUXILIARY_TOOL_APPLY_CARD_APPLICANT,u'领料'),
        (AUXILIARY_TOOL_APPLY_CARD_AUDITOR,u'主管'),
        (AUXILIARY_TOOL_APPLY_CARD_KEEPER,u'发料'),
        (AUXILIARY_TOOL_APPLY_CARD_END,u'完成'),
        (AUXILIARY_TOOL_APPLY_CARD_STOP,u"终止''"),
        )

REFUNDSTATUS_STEEL_CHOICES_REFUNDER = 0
REFUNDSTATUS_STEEL_CHOICES_INSPECTOR = 1
REFUNDSTATUS_STEEL_CHOICES_KEEPER = 2
REFUNDSTATUS_STEEL_CHOICES_END = 3
REFUNDSTATUS_STEEL_CHOICES_STOP = STORAGE_CARD_STOP_STATUS
REFUNDSTATUS_STEEL_CHOICES = (
    (REFUNDSTATUS_STEEL_CHOICES_REFUNDER,u"退库人"),
    (REFUNDSTATUS_STEEL_CHOICES_INSPECTOR,u"检查员"),
    (REFUNDSTATUS_STEEL_CHOICES_KEEPER,u"库管员"),
    (REFUNDSTATUS_STEEL_CHOICES_END,u"结束"),
    (REFUNDSTATUS_STEEL_CHOICES_STOP,u"终止"),
)


REFUNDSTATUS_CHOICES_REFUNDER = 0
REFUNDSTATUS_CHOICES_KEEPER = 1
REFUNDSTATUS_CHOICES_END = 2
REFUNDSTATUS_CHOICES_STOP = STORAGE_CARD_STOP_STATUS
REFUNDSTATUS_CHOICES = (
    (REFUNDSTATUS_CHOICES_REFUNDER,u"退库人"),
    (REFUNDSTATUS_CHOICES_KEEPER,u"库管员"),
    (REFUNDSTATUS_CHOICES_END,u"结束"),
    (REFUNDSTATUS_CHOICES_STOP,u"终止"),
)

STORAGEDEPARTMENT_CHOICES=( 
    (-1,u'------'),
    (1,u'焊一组'),
    (2,u'焊二组'),
    (3,u'焊三组'),
    (4,u'电焊组'),
)

AUTH_TYPE_CHOICES = (
    (0, u"采购管理"),
    (1, u"库存管理"),
    (2, u"生产管理"),
    (3, u"技术资料管理")
)

AUXILIARY_TOOLS_MODELS_CHOICES=(
        (0,u'碳棒'),
        (1,u'面罩'),
        (2,u'白黑玻璃'),
        (3,u'安全帽'),
    )
STORAGE_ENTRY_TYPE_WELD = 0
STORAGE_ENTRY_TYPE_STEEL = 1

STORAGE_ENTRY_TYPECHOICES=(
    (0,u"焊材"),
    (1,u"钢材"),
)

ITEM_STATUS_NORMAL = 0
ITEM_STATUS_SPENT = 1
ITEM_STATUS_OVERDUE = 2
ITEM_STATUS_SCRAPPED = 3
WELD_ITEM_STATUS_CHOICES = (
    (ITEM_STATUS_NORMAL,u"正常使用"),
    (ITEM_STATUS_SPENT,u"已用完"),
    (ITEM_STATUS_OVERDUE,u"已过期"),
    (ITEM_STATUS_SCRAPPED,u"已报废"),
)

#技术资料管理

#for test
capProcessTemplate = [
{"index": u"1", "name": u"下  料", "detail": u"1.1  下料前认真核对钢板的材质、规格，热处理状态，并移植材质标记（不许打钢印）          1.2  封头坯料尺寸 -34×D1850"},
{"index": u"2", "name": u"数控切割", "detail": u"切割坯料外圆，切割前预热 120℃，割后清除熔渣，毛刺等，与R3041.05共带一块母材试板"},
{"index": u"3", "name": u"热压", "detail": u"对封头毛坯热压成形（外协）。"},
{"index": u"4", "name": u"热处理", "detail": u"封头进行恢复材料状态的正火热处理，注意与R3041.05同炉热处理，热处理后母材试板进行力学性能试验，实验结果确认合格后，将部分试板回厂，经复验合格后，再按图纸加工好坡口（外协）。剩余试板随封头回厂。"},
{"index": u"5", "name": u"检 查", "detail": u"5.1.封头表面凹凸量  -6～+12mm；5.2. 封头最小壁厚不得小于27.7mm；      5.3.封头主要尺寸允差见下表规定:大口内直径允差：-4～+5；总高度公差：-3～+4；大口外圆周长公差：-12～+15；大小口同心度：≤2mm。"},
{"index": u"6", "name": u"入 库", "detail": u"检验及试板性能合格后入库。"},
]
cyliderProcessTemplate = [
{"index": u"1", "name": u"预 备", "detail": u"认真核对钢板的材质、规格，并移植材质标记，不许打钢印"},
{"index": u"2", "name": u"切 割", "detail": u"采用数控切割，均分两端下料，1/2下料尺寸：-46×2364-4214(宽度2364两端各含5mm加工余量，长度4214两端各含150mm压头余量)，保证对角线公差不超过2mm"},
{"index": u"3", "name": u"修 磨", "detail": u"割后清除熔渣、毛刺及氧化皮等"},
{"index": u"4", "name": u"划 线", "detail": u"按筒体理论展开长划压头切割线及压制线，并在压头切割线上打样冲"},
{"index": u"5", "name": u"压 头", "detail": u"根据环缝坡口形式确定压弯方向，压制弧度，并用样板检测压制弧度，间隙≤2mm"},
{"index": u"6", "name": u"切 割", "detail": u"封头回厂后确定筒体实际展开长，划出实际压头切割线，用半自动切割机割压头余量，并开对接坡口"},
{"index": u"7", "name": u"修 磨", "detail": u"割后清除熔渣、毛刺及氧化皮等，使其呈现金属光泽，坡口表面不得有裂纹、分层、夹杂等缺陷"},
{"index": u"8", "name": u"探 伤", "detail": u"坡口表面按JB/T4730.4-2005《压力容器无损检测》标准进行100% MT检测，Ⅰ级合格"},
{"index": u"9", "name": u"圈 圆", "detail": u"在中三辊上卷制圆筒，并用样板检测压制弧度，间隙≤2mm"},
{"index": u"10", "name": u"对 接", "detail": u"10.1 纵缝对口错边量b≤2mm，外圆周长允差-3mm≤C≤6mm 10.2 清理坡口两侧表面30mm范围内的氧化物、油污、熔渣、及其它影响焊缝质量的有害杂质"},
{"index": u"11", "name": u"焊 接", "detail": u"筒体纵缝A2、A3的装配点焊与焊接均执行RH09-015007B焊接工艺指导书，并与纵缝焊接试板一同焊接，焊接产品试板执行R05-015007B- -01《压力容器产品试板工艺卡（流转）》"},
{"index": u"12", "name": u"探 伤", "detail": u"对焊接试板进行鉴证。"},
{"index": u"13", "name": u"切 割", "detail": u"将试板从筒体上切割下来，不得伤及筒体，试板交试板库"},
{"index": u"14", "name": u"修 磨", "detail": u"割后清除熔渣、毛刺及氧化皮等"},
{"index": u"15", "name": u"校 圆", "detail": u"用样板检查纵缝处所形成的棱角，E≤3mm；同一断面的最大最小直径差e≤3mm"},
{"index": u"16", "name": u"探 伤", "detail": u"纵缝按JB/T4730-2005《压力容器无损检测》标准进行100% RT检测，Ⅱ级合格，技术等级为AB级；合格后进行≥20%UT检测，Ⅰ级合格，技术等级为B级；焊缝内外表面100%MT检测，Ⅰ级合格"},
{"index": u"17", "name": u"修 磨", "detail": u"使焊缝与母材光滑过渡，焊缝余高不得高于3mm"},
{"index": u"18", "name": u"坡 口", "detail": u"检验合格后按图纸要求机加工出环缝坡口及过渡段（加工坡口前筒体上下端需加工装支撑）。"},
{"index": u"19", "name": u"修 磨", "detail": u"加工后清除毛刺及油污等，坡口表面不得有裂纹、分层、夹杂等缺陷。"},
{"index": u"20", "name": u"探 伤", "detail": u"坡口按JB/T4730-2005《压力容器无损检测》标准执行100% MT检测，I级合格。"},
{"index": u"21", "name": u"入 库", "detail": u"筒体及试板经检验合格后筒体入半成品库。"},
]

H1 = "0"
J = "2"
R = "3"
ZM = "4"
GY = "5"
DY = "6"
XZ = "7"

CIRCULATION_CHOICES = (
    (H1, "H1"),
    (J, "J"),
    (ZM, "ZM"),
    (R, "R"),
    (GY, "GY"),
    (DY, "DY"),
    (XZ, "XZ"),
)

W = "W"
W1 = "W1"
W2 = "W2"
W3 = "W3"
W4 = "W4"
W5 = "W5"
W6 = "W6"
W25 = "W25"
P01 = "P01"
P02 = "P02"
R = "R"
R1 = "R1"
R2 = "R2"
Z = "Z"
H = "H"
M = "M"
L = "L"
Y = "Y"
G = "G"
G1 = "G1"
G2 = "G2"
G3 = "G3"
G4 = "G4"
G5 = "G5"
X = "X"
J = "J"
K = "K"
D2 = "D2"
D = "D"

PROCESSING_CHOICES = (
    (W, "W"),    
    (W1, "W1"),
    (W2, "W2"),
    (W3, "W3"),
    (W4, "W4"),
    (W5, "W5"),
    (W6, "W6"),
    (W25, "W25"),
    (P01, "P01"),
    (P02, "P02"),
    (R, "R"),
    (R1, "R1"),
    (R2, "R2"),
    (Z, "Z"),
    (H, "H"),
    (M, "M"),
    (L, "L"),
    (Y, "Y"),
    (G, "G"),
    (G1, "G1"),
    (G2, "G2"),
    (G3, "G3"),
    (G4, "G4"),
    (G5, "G5"),
    (X, "X"),
    (J, "J"),
    (D, "D"),
    (D2, "D2"),
    (K, "K"),
)

SMAW = "SMAW"
SAW = "SAW"
GMAW = "GMAW"
GTAW = "GTAW"
WELD_METHOD = (
    (SMAW, "焊条电弧焊"),
    (SAW, "埋弧焊"),
    (GMAW, "气体保护焊"),
    (GTAW, "氩弧焊"),
)

WELD_ROD = "weld_rod"
WELD_WIRE = "weld_wire"
WELD_RIBBON = "weld_ribbon"
WELD_FLUX = "weld_flux"
WELD = "weld"
SHEET = "sheet"
PROFILE = "profile"
PURCHASED = "purchased"
OTHER = "other"
STEEL = "steel"
AUXILIARY_TOOL = "auxiliary_tool"
MATERIAL_CATEGORY_CHOICES = (
    (WELD_ROD, u"焊条"),
    (WELD_WIRE, u"焊丝"),
    (WELD_RIBBON, u"焊带"),
    (WELD_FLUX, u"焊剂"),
    (SHEET, u"板材"),
    (PROFILE, u"型材"),
    (PURCHASED, u"外购件"),
    (AUXILIARY_TOOL,u"辅助工具"),
    (OTHER, u"其他"),
)

WELD_TYPE_LIST = [WELD_ROD,WELD_WIRE,WELD_RIBBON,WELD_FLUX]
PURCHASED_TYPE_LIST = [PURCHASED,]
SHEET_TYPE_LIST = [SHEET,]
PROFILE_TYPE_LIST = [PROFILE,]
AUXILIARY_TOOL_TYPE_LIST = [AUXILIARY_TOOL,]
MATERIEL_TYPE_CHOICES = (
    (WELD, u"焊材"),
    (SHEET, u"板材"),
    (PROFILE, u"型材"),
    (PURCHASED, u"外购件"),
    (AUXILIARY_TOOL, u"辅助工具"),
) 

RT = "RT"
UT = "UT"
MT = "MT"
PT = "PT"
VT = "VT"

NONDESTRUCTIVE_INSPECTION_TYPE = (
    (RT, "RT"),
    (UT, "UT"),
    (MT, "MT"),
    (PT, "PT"),
    (VT, "VT"),
)

LOCAL_FACTORY = "0"
INSPECTION_UNIT = "1"
THIRD_PARTY_OR_USER = "2"
WWI_TEST_METHOD_CHOICES = (
    (LOCAL_FACTORY, u"厂内"),
    (INSPECTION_UNIT, u"检验机构"),
    (THIRD_PARTY_OR_USER, u"第三方或用户"),
)

CYLIDER_TRANSFER_CARD = "cylider_transfer_card"
CAP_TRANSFER_CARD = "cap_transfer_card"
WELD_TEST_PLATE_CARD = "weld_test_plate_card"
PARENT_TEST_PLATE_CARD = "parent_test_plate_card"
PRESSURE_PART_TRANSFER_CARD = "pressure_part_transfer_card"
SPECIAL_PART_TRANSFER_CARD = "special_part_transfer_card"
TRANSFER_CARD_TYPE_CHOICES = (
    (CYLIDER_TRANSFER_CARD, u"筒体流转卡"),  
    (CAP_TRANSFER_CARD, u"封头流转卡"),
    (WELD_TEST_PLATE_CARD, u"焊接试板流转卡"),
    (PARENT_TEST_PLATE_CARD, u"母材试板流转卡"),
    (PRESSURE_PART_TRANSFER_CARD, u"受压元件流转卡"),
    (SPECIAL_PART_TRANSFER_CARD, u"特别元件流转卡"),
)


CARD_TYPE_TO_HTML = {
    CYLIDER_TRANSFER_CARD: "techdata/widgets/cylider_transfer_card.html",
    CAP_TRANSFER_CARD: "techdata/widgets/cap_transfer_card.html",
    WELD_TEST_PLATE_CARD: u"techdata/widgets/test_plate_transfer_card.html",
    PARENT_TEST_PLATE_CARD: "techdata/widgets/test_plate_transfer_card.html",
    PRESSURE_PART_TRANSFER_CARD: "techdata/widgets/normal_item_transfer_card.html",
    SPECIAL_PART_TRANSFER_CARD: "techdata/widgets/normal_item_transfer_card.html",
}

MARK_WRITE = "mark_write"
MARK_REVIEW = "mark_review"
MARK_PROOFREAD = "mark_proofread"
MARK_APPROVE = "mark_approve"
MARK_QUOTA = "mark_quota"
MARK_STATISTIC = "mark_statistic"

HEATTREATMENTCARD_ATTR_TEM_START = "temperature_start"
HEATTREATMENTCARD_ATTR_TEM_END = "temperature_end"
HEATTREATMENTCARD_ATTR_TEM_TOP = "temperature_top"
HEATTREATMENTCARD_ATTR_TEM_UP_SPEED = "temperature_up_speed"
HEATTREATMENTCARD_ATTR_TEM_DOWN_SPEED = "temperature_down_speed"
HEATTREATMENTCARD_ATTR_TEM_TIME = "time"

FLUSH_WELD = "FLUSH_WELD"
HORIZONTAL_WELD = "HORIZONTAL_WELD"
OVERHEAD_WELD = "OVERHEAD_WELD"
VERTICAL_WELD = "VERTICAL_WELD"
WIDE_WELD = "WIDE_WELD"

WELD_POSITION_CHOICES = (
    (FLUSH_WELD, u"平焊"),
    (HORIZONTAL_WELD, u"横焊"),
    (OVERHEAD_WELD, u"仰焊"),
    (VERTICAL_WELD, u"立向上焊"),
    (WIDE_WELD, u"全位置焊")
)

#生产管理
PRODUCTION_PLAN_STAUTS_CHOICES = (
    ("",u"---------"),
    (1, u"必保"),
    (2, u"在制"),
)

#焊缝焊接接头  焊工持证项目
SMAW_Fell = "SMAW-Fell-5FG-12/60-Fef3J"
GMAW_Fell = "GMAW-Fell-3G-14-FefS-11/15"
SAW_1G_07 = "SAW-1G07/09/19"
WELD_CERTIFICATION = (
    (SMAW_Fell, "SMAW-Fell-5FG-12/60-Fef3J"),
    (GMAW_Fell, "GMAW-Fell-3G-14-FefS-11/15"),
    (SAW_1G_07, "SAW-1G-07/09/19"),
)
#焊接工艺评定编号
RH24_13_09 = "RH24-13-09"
RH24_13_36 = "RH24-13-36"
PROCEDURE_QUALIFICATION_INDEX = (
    (RH24_13_09, "RH24-13-09"),
    (RH24_13_36, "RH24-13-36"),
)


#标单评论人属性
Z_APPLY_OPERATOR=1
Z_APPLY_LEAD=2
Z_NEED=3
Z_CENTRALIZE=4
Z_LOGISTICAL=5
Z_COMPANY=6
G_OPERATOR=7
G_LEAD=8
G_QUALITY=9
G_ECONOMIC=10
G_COMPREHENSIVE=11
Q_OPERATOR=12
Q_NEED_TECH=13
Q_NEED_LEAD=14
Q_COMPREHENSIVE=15
Q_COMPANY=16

S_MATERIEL=17
S_PROCESS=18
S_WELDING=19
S_DESIGN=20
S_ORIGINAL=21

COMMENT_USER_CHOICE=(
	(Z_APPLY_OPERATOR,u"申请表经办人"),
	(Z_APPLY_LEAD,u"申请表申请主管"),
	(Z_NEED,u"申请表需求单位"),
	(Z_CENTRALIZE,u"申请表归口部门"),
	(Z_LOGISTICAL,u"申请表物流采控"),
	(Z_COMPANY,u"申请表公司意见"),
	(G_OPERATOR,u"审核表经办人"),
	(G_LEAD,u"审核表主管领导"),
	(G_QUALITY,u"审核表质量部"),
	(G_ECONOMIC,u"审核表经济运行部"),
	(G_COMPREHENSIVE,u"审核表综合管理部"),
	(Q_OPERATOR,u"比质卡经办人"),
	(Q_NEED_TECH,u"比质卡需求技术"),
	(Q_NEED_LEAD,u"比质卡需求领导"),
	(Q_COMPREHENSIVE,u"比质卡综合管理"),
	(Q_COMPANY,u"比质卡公司意见"),
    (S_MATERIEL,u"代用材料责任工程师"),
    (S_PROCESS,u"代用工艺责任工程师"),
    (S_WELDING,u"代用焊接责任工程师"),
    (S_DESIGN,u"代用设计责任工程师"),
    (S_ORIGINAL,u"代用原设计单位")
)

COMMENT_USER_QUALITY_DICT={
    "Q_OPERATOR":Q_OPERATOR,
    "Q_NEED_TECH":Q_NEED_TECH,
    "Q_NEED_LEAD":Q_NEED_LEAD,
    "Q_COMPREHENSIVE":Q_COMPREHENSIVE,
    "Q_COMPANY":Q_COMPANY
}
COMMENT_USER_APPLY_DICT={
    "Z_APPLY_OPERATOR":Z_APPLY_OPERATOR,
    "Z_APPLY_LEAD":Z_APPLY_LEAD,
    "Z_NEED":Z_NEED,
    "Z_CENTRALIZE":Z_CENTRALIZE,
    "Z_LOGISTICAL":Z_LOGISTICAL,
    "Z_COMPANY":Z_COMPANY
    
}

COMMENT_USER_SUBSTITUDE_DICT={
    "S_MATERIEL":S_MATERIEL,
    "S_PROCESS":S_PROCESS,
    "S_WELDING":S_WELDING,
    "S_DESIGN":S_DESIGN,
    "S_ORIGINAL":S_ORIGINAL
    
}
COMMENT_USER_CHECK_DICT={
    "G_OPERATOR":G_OPERATOR,
    "G_LEAD":G_LEAD,
    "G_QUALITY":G_QUALITY,
    "G_ECONOMIC":G_ECONOMIC,
    "G_COMPREHENSIVE":G_COMPREHENSIVE
    
}


BIDFORM_PART_STATUS_INVITE_BID_APPLY_FILL=10
BIDFORM_PART_STATUS_INVITE_BID_APPLY_OPERATOR_COMMENT=20
BIDFORM_PART_STATUS_INVITE_BID_APPLY_LEAD_COMMENT=30
BIDFORM_PART_STATUS_INVITE_BID_APPLY_NEED_COMMENT=40
BIDFORM_PART_STATUS_INVITE_BID_APPLY_CENTRALIZE_COMMENT=50
BIDFORM_PART_STATUS_INVITE_BID_APPLY_LOGISTICAL_COMMENT=60
BIDFORM_PART_STATUS_INVITE_BID_APPLY_COMPANY_COMMENT=70

BIDFORM_PART_STATUS_INVITE_BID_CHECK_FILL=80
BIDFORM_PART_STATUS_INVITE_BID_CHECK_OPERATOR_COMMENT=90
BIDFORM_PART_STATUS_INVITE_BID_CHECK_LEAD_COMMENT=100
BIDFORM_PART_STATUS_INVITE_BID_CHECK_QUALITY_COMMENT=110
BIDFORM_PART_STATUS_INVITE_BID_CHECK_ECONOMIC_COMMENT=120
BIDFORM_PART_STATUS_INVITE_BID_CHECK_COMPREHENSIVE_COMMENT=130

BIDFORM_PART_STATUS_INVITE_BID_QUALITY_FILL=140
BIDFORM_PART_STATUS_INVITE_BID_QUALITY_OPERATOR_COMMENT=150
BIDFORM_PART_STATUS_INVITE_BID_QUALITY_NEED_TECH_COMMENT=160
BIDFORM_PART_STATUS_INVITE_BID_QUALITY_NEED_LEAD_COMMENT=170
BIDFORM_PART_STATUS_INVITE_BID_QUALITY_COMPREHENSIVE_COMMENT=180
BIDFORM_PART_STATUS_INVITE_BID_QUALITY_COMPANY_COMMENT=190
BIDFORM_PART_STATUS_INVITE_BID_APPLY_FINISH=200


MATERIEL_SUBSTITUDE_FILL=300
MATERIEL_SUBSTITUDE_MATERIEL=310
MATERIEL_SUBSTITUDE_PROCESS=320
MATERIEL_SUBSTITUDE_WELDING=330
MATERIEL_SUBSTITUDE_DESIGN=340
MATERIEL_SUBSTITUDE_ORIGINAL=350
MATERIEL_SUBSTITUDE_FINISH=360

MATERIEL_SUBSTITUDE_STATUS_DICT={
    "FILL":MATERIEL_SUBSTITUDE_FILL,
    "MATERIEL":MATERIEL_SUBSTITUDE_MATERIEL,
    "PROCESS":MATERIEL_SUBSTITUDE_PROCESS,
    "WELDING":MATERIEL_SUBSTITUDE_WELDING,
    "DESIGN":MATERIEL_SUBSTITUDE_DESIGN,
    "ORIGINAL":MATERIEL_SUBSTITUDE_ORIGINAL
    
}

BIDFORM_INVITE_BID_APPLY_DIC={
    "FILL":BIDFORM_PART_STATUS_INVITE_BID_APPLY_FILL,
    "OPERATOR_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_APPLY_OPERATOR_COMMENT,
    "LEAD_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_APPLY_LEAD_COMMENT,
    "NEED_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_APPLY_NEED_COMMENT,
    "CENTRALIZE_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_APPLY_CENTRALIZE_COMMENT,
    "LOGISTICAL_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_APPLY_LOGISTICAL_COMMENT,
    "COMPANY_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_APPLY_COMPANY_COMMENT
}

BIDFORM_INVITE_BID_SUPPLIER_DIC={
    "FILL":BIDFORM_PART_STATUS_INVITE_BID_CHECK_FILL,
    "OPERATOR_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_CHECK_OPERATOR_COMMENT,
    "LEAD_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_CHECK_LEAD_COMMENT,
    "QUALITY":BIDFORM_PART_STATUS_INVITE_BID_CHECK_QUALITY_COMMENT,
    "ECONOMIC_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_CHECK_ECONOMIC_COMMENT,
    "COMPREHENSIVE":BIDFORM_PART_STATUS_INVITE_BID_CHECK_COMPREHENSIVE_COMMENT
}

BIDFORM_INVITE_BID_QUALITY_DIC={
    "FILL":BIDFORM_PART_STATUS_INVITE_BID_QUALITY_FILL,
    "OPERATOR_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_QUALITY_OPERATOR_COMMENT,
    "TECH_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_QUALITY_NEED_TECH_COMMENT,
    "LEAD_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_QUALITY_NEED_LEAD_COMMENT,
    "COMPREHENSIVE_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_QUALITY_COMPREHENSIVE_COMMENT,
    "COMPANY_COMMENT":BIDFORM_PART_STATUS_INVITE_BID_QUALITY_COMPANY_COMMENT
}
COMMENT_STATUS_CHOICES=(
	(BIDFORM_PART_STATUS_INVITE_BID_APPLY_FILL,u"申请表填写"),
	(BIDFORM_PART_STATUS_INVITE_BID_APPLY_OPERATOR_COMMENT,u"申请经办人意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_APPLY_LEAD_COMMENT,u"申请表申请领导意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_APPLY_NEED_COMMENT,u"申请表需求部门意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_APPLY_CENTRALIZE_COMMENT,u"申请表归口部门意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_APPLY_LOGISTICAL_COMMENT,u"申请表物流采控部门意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_APPLY_COMPANY_COMMENT,u"申请表公司意见"),

	(BIDFORM_PART_STATUS_INVITE_BID_CHECK_FILL,u"审核表填写"),
	(BIDFORM_PART_STATUS_INVITE_BID_CHECK_OPERATOR_COMMENT,u"审核表经办人意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_CHECK_LEAD_COMMENT,u"审核表主管领导意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_CHECK_QUALITY_COMMENT,u"审核表质量部意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_CHECK_ECONOMIC_COMMENT,u"审核表经济运行部意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_CHECK_COMPREHENSIVE_COMMENT,u"审核表综合管理部意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_QUALITY_FILL,u"比质卡填写"),
	(BIDFORM_PART_STATUS_INVITE_BID_QUALITY_OPERATOR_COMMENT,u"比质卡经办人意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_QUALITY_NEED_TECH_COMMENT,u"比质卡需求技术意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_QUALITY_NEED_LEAD_COMMENT,u"比质卡需求领导意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_QUALITY_COMPREHENSIVE_COMMENT,u"比质卡综合管理意见"),
	(BIDFORM_PART_STATUS_INVITE_BID_QUALITY_COMPANY_COMMENT,u"比质卡公司意见"),
    (MATERIEL_SUBSTITUDE_FILL,u"代用单填写"),
    (MATERIEL_SUBSTITUDE_MATERIEL,u"材料工程师"),
    (MATERIEL_SUBSTITUDE_PROCESS,u"工艺工程师"),
    (MATERIEL_SUBSTITUDE_WELDING,u"焊接工程师"),
    (MATERIEL_SUBSTITUDE_DESIGN,u"设计工程师"),
    (MATERIEL_SUBSTITUDE_ORIGINAL,u"原设计单位"),
    (MATERIEL_SUBSTITUDE_FINISH,u"材料代用结束"),
    (BIDFORM_PART_STATUS_INVITE_BID_APPLY_FINISH,u"结束")
)


BID_APPLY=1
SUPPLIER_CHECK=2
QUALITYPRICECARD=3
MATERIEL_SUBSTITUDE=4

BID_APPLY_TYPE_CHOICES=(
    (BID_APPLY,u"招标申请表"),
    (SUPPLIER_CHECK,u"供应商审核表"),
    (QUALITYPRICECARD,u"比质比价卡"),
    (MATERIEL_SUBSTITUDE,u"材料代用表")
)

SupplierCChoices=(
    (0,u"实体"),
    (1,u"贸易")
)

SYNSIZE_FILE_LIST_STATUS = [
    "sketch","pressure_test","craph","product","encasement_graph","mark","encasement_list","coating_detail"

]

IMATERIEL = 0
IPROCESS = 1
IFEEDING = 2
IBARREL = 3
IASSEMBLE = 4
IPRESSURE = 5
IFACADE = 6

INSPECT_CATEGORY_CHOICE = (
    (IMATERIEL, u"材料检验"),
    (IPROCESS, u"工序检验"),
    (IFEEDING, u"零件投料检验"),
    (IBARREL, u"封头/筒体检验"),
    (IASSEMBLE, u"装配检验"),
    (IPRESSURE, u"压力试验"),
    (IFACADE, u"外观检验"),
)

UnCheck=0
CheckPass=1
CheckUnPass=2
FINISHED=3
QA_STATUS=(
    (UnCheck, u'未检验'),
    (CheckPass, u'检验通过'),
    (CheckUnPass, u'检验为通过'),
    (FINISHED, u"已完成")
)

UNDILIVER=0
DILIVER=1
DILIVER_STATUS=(
    (UNDILIVER, u'未交货'),
    (DILIVER, u'交货')
)
