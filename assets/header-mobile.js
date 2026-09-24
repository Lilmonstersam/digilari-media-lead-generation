(function($) {
  "use strict";

  	/* ========================================== 
	Sticky Header 1
	========================================== */
	$(window).on("scroll", function(){
		if ( $( '#site-header' ).hasClass( "sticky-header" ) ) {
			var header_height = $('#site-header').outerHeight() + 30;	
			
		    if ($(window).scrollTop() >= header_height) {	    	
		        $('.mobile-header-sticky .header_mobile').addClass('is-stuck');	        
		    }else {
		        $('.mobile-header-sticky .header_mobile').removeClass('is-stuck');		              
		    }
		}
	});

	var site_header = $('.sticky-header');
	if( !site_header.hasClass('header-overlay') ){
		site_header.append('<div class="header-clone"></div>');
		$('.header-clone').height(site_header.find('.octf-main-header').outerHeight());
		site_header.find('.header-clone').hide();	
	}
	$(window).on("scroll", function(){
		var header_height = site_header.outerHeight();	
			
		if ($(window).scrollTop() >= header_height) {	    	
			site_header.find('.octf-main-header').addClass('is-stuck');	
			site_header.find('.header-clone').show();	
		}else {
			site_header.find('.octf-main-header').removeClass('is-stuck');		              
			site_header.find('.header-clone').hide();	
		}
	});
	/* ========================================== 
	Search on Header
	========================================== */
	$('.toggle_search').on("click", function(){
		$(this).toggleClass( "active" );
        $('.h-search-form-field').toggleClass('show');
        if ($(this).find('i').hasClass( "flaticon-search" )) {
       		$('.toggle_search > i').removeClass( "flaticon-search" ).addClass("flaticon-delete");
        }else{
       		$('.toggle_search > i').removeClass( "flaticon-delete" ).addClass("flaticon-search");
        }
        $('.h-search-form-inner > form > input.search-field').focus();
    });

    /* ========================================== 
	Header Mobile
	========================================== */
	/* mobile_mainmenu create span */
	$('.mobile_mainmenu li:has(ul)').prepend('<span class="arrow"><i class="flaticon-arrow-point-to-right"></i></span>');

	$( "#mmenu_toggle" ).on('click', function() {
		$(this).toggleClass( "active" );
		$(this).parents('.header_mobile').toggleClass( "open" );
		if ($(this).hasClass( "active" )) {
			$('.mobile_nav').stop(true, true).slideDown();
		}else{
			$('.mobile_nav').stop(true, true).slideUp();
		}		
	});

	$(".mobile_mainmenu > li span.arrow").click(function() {
        $(this).parent().find("> ul").stop(true, true).slideToggle()
        $(this).toggleClass( "active" ); 
    });

	/* ========================================== 
	Back To Top
	========================================== */
    if ($('#back-to-top').length) {
	    var scrollTrigger = 500, // px
	        backToTop = function () {
	            var scrollTop = $(window).scrollTop();
	            if (scrollTop > scrollTrigger) {
	                $('#back-to-top').addClass('show');
	            } else {
	                $('#back-to-top').removeClass('show');
	            }
	        };
	    backToTop();
	    $(window).on('scroll', function () {
	        backToTop();
	    });
	    $('#back-to-top').on('click', function (e) {
	        e.preventDefault();
	        $('html,body').animate({
	            scrollTop: 0
	        }, 700);
	    });	
    };

})(jQuery);