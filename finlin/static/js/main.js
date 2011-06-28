function createQuote(elem){
    var paper = new Raphael(elem, 32, 29);
    var quote = paper.path("M14.505,5.873c-3.937,2.52-5.904,5.556-5.904,9.108c0,1.104,0.192,1.656,0.576,1.656l0.396-0.107c0.312-0.12,0.563-0.18,0.756-0.18c1.128,0,2.07,0.411,2.826,1.229c0.756,0.82,1.134,1.832,1.134,3.037c0,1.157-0.408,2.14-1.224,2.947c-0.816,0.807-1.801,1.211-2.952,1.211c-1.608,0-2.935-0.661-3.979-1.984c-1.044-1.321-1.565-2.98-1.565-4.977c0-2.259,0.443-4.327,1.332-6.203c0.888-1.875,2.243-3.57,4.067-5.085c1.824-1.514,2.988-2.272,3.492-2.272c0.336,0,0.612,0.162,0.828,0.486c0.216,0.324,0.324,0.606,0.324,0.846L14.505,5.873zM27.465,5.873c-3.937,2.52-5.904,5.556-5.904,9.108c0,1.104,0.192,1.656,0.576,1.656l0.396-0.107c0.312-0.12,0.563-0.18,0.756-0.18c1.104,0,2.04,0.411,2.808,1.229c0.769,0.82,1.152,1.832,1.152,3.037c0,1.157-0.408,2.14-1.224,2.947c-0.816,0.807-1.801,1.211-2.952,1.211c-1.608,0-2.935-0.661-3.979-1.984c-1.044-1.321-1.565-2.98-1.565-4.977c0-2.284,0.449-4.369,1.35-6.256c0.9-1.887,2.256-3.577,4.068-5.067c1.812-1.49,2.97-2.236,3.474-2.236c0.336,0,0.612,0.162,0.828,0.486c0.216,0.324,0.324,0.606,0.324,0.846L27.465,5.873z")
    quote.attr({'fill': '#666', 'stroke':'none'})
    return quote
}

$("a.full-strategy").click(function(event){  
    event.preventDefault()
    clicked = $(this)
    container = $('<p>');
    container.insertAfter(clicked); 
    clicked.remove()
    href = clicked.attr('href')

    $.ajax({
      url: href,
      success: function(data){
        data = $(data)
        extracted = data.find('#container')
        
        elem = extracted.find('.left_quote')
        left_quote = createQuote(elem.get()[0]) 

        //have to do right quote different bc it has to be slipped into previous sibling
        elem = extracted.find('.right_quote')
        previous = elem.prev()
        previous.addClass('clearfix') //otherwise renders funny
        previous.append(elem)

        right_quote = createQuote(elem.get()[0]) 
        right_quote.rotate(180)

        container.prepend(extracted).hide()
        container.fadeIn('slow')
 
      }
    });
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

