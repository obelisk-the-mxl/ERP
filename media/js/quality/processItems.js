$(document).on("change", "#id_work_order", function() {
    order_id = $(this).val();
    alert(order_id);
    Dajaxice.quality.get_subworkorder(get_subworkorder_callback, {
        "order_id": order_id,
    });
});

function get_subworkorder_callback(data) {
    $("#sub_order_span").html(data);
}

function refresh() {
    sub_work_order = $("#sub_work_order").val();
    Dajaxice.quality.getProcessingItems(getProcessing_callback, {
        "sub_work_order": sub_work_order
    });
}

function getProcessing_callback(data) {
    $("#Processing_items_table").html(data.html);
}

$(".unpass").click(function(){
    process_ids = Array();
    $("input.checkbox").each(function(){
        process_ids.push($(this).attr("args"));
    });
    cate = $(this).attr("cate");
    Dajaxice.quality.addUncheckBill(add_unpassbill_callback, 
        {
            "process_detail_ids": process_ids,
            "cate": cate
        })
});

function add_unpassbill_callback(data) {
    ids = data.success_ids;
    cate = data.cate;
    if (cate == "repair") {
        text = "已加入退修单";
    }
    else if (cate == "unquality") {
        text = "已加入不合格单";
    }
    else {
        text = "已加入报废单";
    }
    for (idx in ids) {
        id = ids[idx];
        $("#unpass" + id).parent.html(text);
    }
}

$(document).on("dblclick", "#processing_table tbody tr", function() {
    iid = $(this).attr("iid");
    $("#processing_modal").attr("iid", iid);
    $("#processing_modal").modal();
});

$(document).on("click", "#save_item_form", function(){
    inspect_from = $("#inspect_item_form").serialize();
    iid = $("#processing_modal").attr("iid");
    Dajaxice.quality.updateProcessingItem(updateItem_callback,
        {
            "item_id": iid,
            "inspect_item_form": inspect_from,
        });
});

function updateItem_callback(data) {
    refresh(); 
}

$("#edit_report_btn").click(function(){
   $("#processing_report_modal").modal(); 
});

$("#save_report_form").click(function() {
    order = $("id_work_order").val();
    form = $("#inspect_report_form").serialize();
    Dajaxice.quality.updateProcessingReport(updateProcessingReport_callback, {
        "id_work_order": order_id,
        "inspect_report_form": inspect_report_form
    });
});

function updateProcessingReport_callback(data) {
    
}
