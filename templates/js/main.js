

function setCookie(uid,value,exp_days) {
    let d = new Date();
    d.setTime(d.getTime() + (exp_days*24*60*60*1000));
    let expires = "expires=" + d.toGMTString();
    let user = $("#User").val();
    document.cookies = user + "=" + value + ";" + expires + ";path=/";
}

(function ($) {
    "use strict";


    /*==================================================================
    [ Focus input ]*/
    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
  


})(jQuery);
