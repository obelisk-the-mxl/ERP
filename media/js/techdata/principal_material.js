$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh(){
    var id_work_order = $("#id_work_order").val();
    var inventory_type = $(".form-search").attr("itype");
    Dajaxice.techdata.getInventoryTables(refreshCallBack, {"id_work_order": id_work_order, "inventory_type": inventory_type});
}
function refreshCallBack(data) {
    $(".widget-box").html(data);
}

$("#btn_save_principal").click(function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.addSinglePrincipalItem(function(data) {
        if(data == "ok") {
            alert("保存成功");
            refresh();
        }
        else alert("保存失败");
    }, {
        "id_work_order": id_work_order,
        "form": $("#principal_form").serialize(),
    })
});
$(document).on("click", ".btn-remove", function(){
    if (confirm("是否确定删除？")) {
        var inventory_type = $(".form-search").attr("itype");
        var iid = $(this).parent().parent().attr("iid");
        Dajaxice.techdata.deleteSingleItem(function() {
            alert("删除成功！");
            refresh();
        }, {"iid": iid,  "inventory_type": inventory_type});
    }
});

$(document).on("click", ".btn-mark", function() {
    mark_span = $(this).parent();
    var inventory_type = $(".form-search").attr("itype");
    var id_work_order = $("#id_work_order").val();
    var step = $(this).attr("args");
    Dajaxice.techdata.detailMark(markCallBack, {"id_work_order": id_work_order, 
                                     "step": step, 
                                     "inventory_type": inventory_type,
    });
});
function markCallBack(data) {
    if(data.ret) {
        mark_span.html(data.mark_user);
    }
    else {
        alert(data.warning);
    }
}


