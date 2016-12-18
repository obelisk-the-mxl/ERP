function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.quality.getFeedingItemsTable(
        refreshCallBack,
        {
            "id_work_order" : 1,
        }
    );
}
function refreshCallBack(data) {
    $("#div_report").html(data.html);
}

$(document).on("dblclick", "#div_report tbody .feeding_row", function() {
    $("#feeding_item_modal").modal();
});
