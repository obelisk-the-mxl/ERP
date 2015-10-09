function hide_extra_form(){
    $("#id_bidform").hide();
    $("#id_following_date").hide();
    $("#id_executor").hide();
}

$("#add_process_following").click(function(){
    $("#process_info_form").ajaxSubmit({
        url:"/purchasing/processfollowingadd",
        type:"POST",
        clearForm:true,
        resetForm:true,
        error:function(data){

        },
        success:function(data){
            if(data.status===0){
                alert("添加成功");
                window.location.reload();
            }
            else{
                $("#add_form").html(data.form_html);
                hide_extra_form();
            }
        }

    });
});

function add_process_callback(data){
    alert("成功");
}

$("#add").click(function(){
   hide_extra_form(); 
});
