$(document).ready(function () {
    size_li = $("#myList div#itemList").length;
    x=4;
    $('#myList div#itemList:lt('+x+')').show();
    $('#showMore').click(function () {
        x= (x+8 <= size_li) ? x+8 : size_li;
        $('#myList div#itemList:lt('+x+')').slideDown(500);
    });
    $('#showLess').click(function () {
        x=(x-8<1) ? 4 : x-8;
        $('#myList div#itemList').not(':lt('+x+')').hide(500);
    });
});