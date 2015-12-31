$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh(){
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getProcessBOM(refreshCallBack, {"id_work_order": id_work_order, });
}
function refreshCallBack(data) {
    $("#widget-box").html(data);
}


$(document).on("click", ".tr_materiel", function() {
    var iid = $(this).attr("iid");
    $("#card_modal").attr("iid", iid);
    Dajaxice.techdata.getMaterielInfo(getInfoCallBack, {"iid": iid});
    Dajaxice.techdata.getProcess(getProcessCallBack, {"iid": iid});
});
function getInfoCallBack(data) {
    $("#base-info-area").html(data);
}
function getProcessCallBack(data) {
    $("#process_table").html(data);
}

$("#id_add_process").click(function() {
    var process_id = $("#id_process").val();
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.addProcess(refreshProcess, {"process_id": process_id, "iid": iid, });
});

$(document).on("click", ".btn-del-process", function() {
    var pid = $(this).attr("pid");
    Dajaxice.techdata.deleteProcess(refreshProcess, {"pid": pid});
});

function refreshProcess() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.getProcess(getProcessCallBack, {"iid": iid});
}


$("#weldseam_edit").click(function() {
    Dajaxice.techdata.getWeldSeamCard(getCardCallBack, {}); 
});
function getCardCallBack(data) {
    $("#weld_seam_card").html(data);
}

$(document).on("click", "#btn_cancel", function() {
    $("#weld_seam_card").html("");
});


$(document).on("click", "#btn_weldseam_confirm", function() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.addWeldSeam(addWeldSeamCallBack, {"iid": iid, "form": $("#weld_seam_card").serialize()})
});
function addWeldSeamCallBack(data) {
    if(data == "ok") {
        alert("焊缝添加成功！");
        $("#weld_seam_card").html("");
    }
    else {
        $("#weld_seam_card").html(data);
    }
}
