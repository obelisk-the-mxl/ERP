$(document).on("dblclick", ".assemble-input", function() {
    child = $(this).children().get(0);
    text = $(this).text();
    if (child == null) {
        $(this).html(
            "<input type='text' class='input-small' style='margin-bottom:0px'>"
        )
        child = $(this).children().get(0);
        if (text != "") {
            $(child).val(text);
        }
        $(child).on("blur", function(){
            v = $(this).attr("value");
            $(this).parent().html(v);
        });
    }
});


$(document).on("dblclick", ".conclusion-input", function() {
    child = $(this).children().get(0);
    text = $(this).text();
    if (child == null) {
        $(this).html(
            "<input type='text' class='input-xlarge' style='margin-bottom:0px'>"
        )
        child = $(this).children().get(0);
        if (text != "") {
            $(child).val(text);
        }
        $(child).on("blur", function(){
            v = $(this).attr("value");
            $(this).parent().html(v);
        });
    }
});

