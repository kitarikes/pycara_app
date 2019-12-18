$(function() {
    var hoge = $(".sub").text();
    if ( hoge == "chemistry"){
        $(".color").css({background:'#7fffd4'});
    }else if(hoge == "history"){
        $(".color").css({background:'#ff8c00'});
    }else if(hoge == "english"){
        $(".color").css({background:'#ba55d3'});
    }else if(hoge == "math"){
        $(".color").css({background:'#00bfff'});
    };
});