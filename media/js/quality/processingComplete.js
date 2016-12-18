function refesh() {
    sub_work_order_id = $("#order_span").text();
    Dajaxice.quality.getProcessComplete(getProcessComplete_callback, {
        "sub_work_order_id": sub_work_order_id
    });
}

function getProcessComplete_callback(data) {
    $("#progress_div").html(data.html);
}
