$(document).ready(refresh);

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
