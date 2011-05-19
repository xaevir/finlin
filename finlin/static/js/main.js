//must be the original dimensions
w = 35
h = 41

if ($("#home").length == 0) {
    dim = .8
}
else {
    dim = 3
}

var paper = new Raphael(document.getElementById('logo-svg'), w*dim, h*dim);  

var inner = paper.path("M17.239,39.167c-1.29-1.074-4.528-3.873-7.729-7.455"
        +"c-2.392-2.676-4.293-5.256-5.652-7.67c-1.659-2.948-2.5-5.635-2.5-7.988c0-2.542,0.419-4.81,1.246-6.74"
        +"c0.766-1.787,1.891-3.308,3.343-4.52c2.729-2.275,6.633-3.478,11.293-3.478c4.659,0,8.563,1.203,11.292,3.478"
        +"c1.453,1.211,2.578,2.732,3.344,4.52c0.827,1.931,1.246,4.198,1.246,6.74c0,2.353-0.841,5.04-2.501,7.988"
        +"c-1.358,2.414-3.26,4.994-5.652,7.67C21.768,35.294,18.528,38.093,17.239,39.167L17.239,39.167Z")

inner.attr({'fill': '90-#fff-#fff', 'stroke':'none'})
//scale has to be a string if used in above attr
inner.scale(dim, dim, 0, 0)

//EC7403-#FBB300-#EC7403

var lion = paper.set();
lion.push(
    paper.rect(13.442, 14.091, 0.899, 7.669),
    paper.path("M20.567,26.647 L19.931,27.18 L13.442,21.756 L14.079,21.225Z"),
    paper.path("M14.338,14.089 L13.703,14.621 L10.587,12.018 L11.224,11.486Z"),
    paper.rect(19.71, 14.091, 0.899, 7.669),
    paper.path("M13.485,26.647 L14.121,27.18 L20.609,21.756 L19.973,21.225Z"),
    paper.path("M19.713,14.089 L20.349,14.621 L23.465,12.018 L22.828,11.486Z"),
    paper.path("M20,21.465 L17.034,23.913 L14.067,21.465"),
    paper.rect(9.77, 16.045, 0.899, 7.67),
    paper.path("M17.665,29.251 L17.029,29.783 L9.77,23.71 L10.406,23.179Z"),
    paper.path("M10.666,16.043 L10.029,16.575 L6.915,13.972 L7.55,13.44Z"),
    paper.rect(23.382, 16.045, 0.899, 7.67),
    paper.path("M16.405,29.241 L17.041,29.773 L24.281,23.71 L23.646,23.179Z"),
    paper.path("M23.386,16.043 L24.022,16.575 L27.137,13.972 L26.501,13.44Z"),
    paper.path("M26.453,5.411 L27.278,5.484 L27.641,9.528 L26.814,9.455Z"),
    paper.path("M27.351,6.308 L27.276,5.482 L23.232,5.12 23.307,5.946Z"),
    paper.path("M7.645,5.411 L6.819,5.484 L6.458,9.528 L7.283,9.455Z"),
    paper.path("M6.747,6.308 L6.821,5.482 L10.865,5.12 L10.791,5.946"),
    paper.path("M17.239,0.378C7.95,0.378,0.42,5.008,0.42,16.054s16.819,24.324,16.819,24.324S34.059,27.1,34.059,16.054"
        +"S26.527,0.378,17.239,0.378L17.239,0.378z M17.239,39.167c-1.29-1.074-4.528-3.873-7.729-7.455"
        +"c-2.392-2.676-4.293-5.256-5.652-7.67c-1.659-2.948-2.5-5.635-2.5-7.988c0-2.542,0.419-4.81,1.246-6.74"
        +"c0.766-1.787,1.891-3.308,3.343-4.52c2.729-2.275,6.633-3.478,11.293-3.478c4.659,0,8.563,1.203,11.292,3.478"
        +"c1.453,1.211,2.578,2.732,3.344,4.52c0.827,1.931,1.246,4.198,1.246,6.74c0,2.353-0.841,5.04-2.501,7.988"
        +"c-1.358,2.414-3.26,4.994-5.652,7.67C21.768,35.294,18.528,38.093,17.239,39.167L17.239,39.167Z")
    )

lion.attr({'stroke': 'none', 'fill':'#000'})
lion.scale(dim, dim, 0, 0)

/*
var lion_clone = lion.clone();
lion_clone.attr({'stroke': 'none', 'fill':'#00A1FF'})
lion_clone.toBack();
*/
/*inner.toBack();*/

/*
var lion_clone2 = lion.clone();
lion_clone2.attr({'stroke': 'none', 'fill':'#000'})
lion_clone2.translate(0, 1.5);
lion_clone2.toBack();
*/

/*var lion_clone3 = lion.clone();
lion_clone3.attr({'stroke': 'none', 'fill':'#000'})
lion_clone3.translate(0, 2);
lion_clone3.toBack();
*/

/*lion_clone.attr('fill':'#00A1FF')
inner_clone.attr('fill':'#00A1FF')
lion_clone.translate(1, 1);
inner_clone.translate(1, 1);
*/

/*$("#logo").hover(
  function () {
    inner.attr({'stroke': '#FE7300'})
    lion.attr({'fill': '#B1DAF3'})
  }, 
  function () {
    lion.attr({'fill': '#FE7300'})
    inner.attr({'fill': '#fff'})
  }
);
*/





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

