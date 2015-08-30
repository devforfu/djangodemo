/*bootstrap hover***************/

    $(function() {
        $(".dropdown").hover(
            function(){ $(this).addClass('open') },
            function(){ $(this).removeClass('open') }
        );
    });






$('#myCarousel').carousel({
		interval:   4000
	});
	


$(function(){
 
$(document).on( 'scroll', function(){
 
if ($(window).scrollTop() > 100) {
$('.scroll-top-wrapper').addClass('show');
} else {
$('.scroll-top-wrapper').removeClass('show');
}
});
 
$('.scroll-top-wrapper').on('click', scrollToTop);
});
 
function scrollToTop() {
verticalOffset = typeof(verticalOffset) != 'undefined' ? verticalOffset : 0;
element = $('body');
offset = element.offset();
offsetTop = offset.top;
$('html, body').animate({scrollTop: offsetTop}, 500, 'linear');
}





jQuery('nav').on('click', 'a[data-toggle="tab"]',  function(e){
    e.preventDefault();
    alert(this);
});



