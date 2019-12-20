
$(function(){
    // 「id="jQueryBox"」を非表示

    $("#jQueryBox").css("display", "none");

 
    // 「id="jQueryPush"」がクリックされた場合
    $(".jQueryPush").click(function(){
        
        // 「id="jQueryBox"」の表示、非表示を切り替える
        $("#jQueryBox").toggle();
        
    });
});
