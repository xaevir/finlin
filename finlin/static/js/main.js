$("#load_basic").click(function(){  
    $("#result").html(ajax_load).load(loadUrl);  
});  



// Comment Body
$('textarea[name="comment"]').val('more text');

$('textarea[name="comment"]').focus(function() {
    if ($(this).val() == "Comment") {
        $(this).val("");
    };
    //$(this).addClass("focus");
});
$('#comment').blur(function() {
    if ($(this).val() == "") {
        $(this).val("Comment");
    };
    //$(this).removeClass("focus");
});

