( function( $ ) {
    'use strict';

    function rtl_slick(){
        if ($('body').hasClass("rtl")) {
           return true;
        } else {
           return false;
        }
    };

    /* --------------------------------------------------
	 * counter
	 * --------------------------------------------------*/
    var icounter = function () {
    	$('.ot-counter').each(function() {
    		var pos_y   = $(this).offset().top - window.innerHeight;
            var $this   = $(this).find('span.num'),
                countTo = $this.attr('data-to'),
                during  = parseInt( $this.attr('data-time') ),
                topOfWindow = $(window).scrollTop();

            if ( pos_y < topOfWindow ) {    
	            $({
	                countNum: $this.text()
	            }).animate({
	                countNum: countTo
	            },
	            {
	                duration: during,
	                easing: 'swing',
	                step: function() {
	                    $this.text(Math.floor(this.countNum));
	                },
	                complete: function() {
	                    $this.text(this.countNum);
	                }
	            });
	        }
        });
    };

    var counter = function () {
		icounter();
		$(window).on('scroll', function() {
			icounter();
		});
	};

    /* --------------------------------------------------
	 * progress bar
	 * --------------------------------------------------*/
	function lineProgress() {
		$('.ot-progress').each(function() {
			var pos_y = $(this).offset().top;
			var value = $(this).find(".progress-bar").data('percent');
			var topOfWindow = $(window).scrollTop();
			if (pos_y < topOfWindow + 900) {
				$(this).find(".progress-bar").css({
					'width': value
				}, "slow");
			}
		});
	};

    function circleProgress() {
        $('.circle-progress').each(function() {
            var bar_color1 = $(this).data('color1');
            var bar_color2 = $(this).data('color2');
            var pos_y = $(this).offset().top;
            var topOfWindow = $(window).scrollTop();
            if (pos_y < topOfWindow + 900) {
                $(this).find('.inner-bar').easyPieChart({
                    barColor: function(percent) {
                            var ctx = this.renderer.getCtx();
                            var gradient = ctx.createLinearGradient(45,0,0,90);
                                gradient.addColorStop(0, bar_color1);
                                gradient.addColorStop(1, bar_color2);
                            return gradient;
                        },
                    trackColor: false,
                    scaleColor: false,
                    lineCap: 'round',
                    lineWidth: 20,
                    size: 195,
                    animate: 1000,
                    onStart: $.noop,
                    onStop: $.noop,
                    easing: 'easeOutBounce',
                    onStep: function(from, to, percent) {
                        $(this.el).find('.percent').text(Math.round(percent)) + '%';
                    }
                });
            }
        });
    };
	
	var progressBar = function () {
		lineProgress();
		circleProgress();
		$(window).on('scroll', function() {
			lineProgress();
			circleProgress();
		});
	};

	/* --------------------------------------------------
	* tabs
	* --------------------------------------------------*/
	var customTabs = function () {

		$('.ot-tabs').each(function() {
			$(this).find('.tabs-heading li').first().addClass('current');
			$(this).find('.tab-content').first().addClass('current');
		});

		$('.tabs-heading li').on( 'click', function(){
			var tab_id = $(this).attr('data-tab');
			$(this).siblings().removeClass('current');
			$(this).parents('.ot-tabs').find('.tab-content').removeClass('current');
			$(this).addClass('current');
			$("#"+tab_id).addClass('current');
		});
	};

	/* --------------------------------------------------
	* accordions
	* --------------------------------------------------*/
	var customAccordions = function () {
        $('.ot-accordions').each( function () {
            var allPanels = $(this).find('.acc-content');
    		$(this).find('.acc-toggle').on( 'click', function(){

                var $this = $(this),
                    $target = $this.next();

                if(!$target.hasClass('active')){
                    allPanels.removeClass('active').slideUp(300);
                    allPanels.parent().removeClass('current');
                    $target.addClass('active').slideDown(300);
                    $target.parent().addClass('current');
                }

                return false;
            });
            $(this).find('.acc-toggle:first').trigger('click');
        });
	};

	/* --------------------------------------------------
	* testimonials
	* --------------------------------------------------*/
    var testimonialSlider = function ( $scope , $ ) {
        $scope.find('.ot-testimonials-slider').each( function () {
            var $selector = $(this),
                $arr      = $selector.data('arrow'),
                $dots     = $selector.data('dots'),
                $nav      = $selector.parents('.onum-row-flex').find('.testicustom-slider-nav'),
                $nav2     = $selector.parents('.onum-row-flex').find('.slider__arrows');
			if( $nav.length > 0 ){var customArrows = $nav;}else{var customArrows = $nav2;}
            $selector.not( '.slick-initialized' ).slick({
                rtl: rtl_slick(),
                slidesToShow: 1,
                slidesToScroll: 1,
                arrows: $arr,
                dots: $dots,
                autoplay: true,
                autoplaySpeed: 6000,
                adaptiveHeight: true,
                fade: true,                
                appendArrows: customArrows,                
                prevArrow: '<button type="button" class="prev-nav"><i class="flaticon-arrow-pointing-to-left"></i></button>',
                nextArrow: '<button type="button" class="next-nav"><i class="flaticon-arrow-pointing-to-right"></i></button>',
            });
        });
    };

    /* --------------------------------------------------
	* message box
	* --------------------------------------------------*/
	var messageBox = function(){
		$('.message-box > i').on( 'click', function() {
			$(this).parent().fadeOut();
		});
	};

	/* --------------------------------------------------
	* projects filter isotope
	* --------------------------------------------------*/
    var projectsFilter = function ( $scope , $ ) {
        $scope.find('.projects-grid').each( function(){
            var $container = $(this); 
            $container.isotope({ 
                itemSelector : '.project-item', 
                animationEngine : 'css',
                masonry: {
                    columnWidth: '.grid-sizer'
                },
            });

            var $optionSets = $('.project_filters'),
                $optionLinks = $optionSets.find('a');

            $optionLinks.on('click', function(){
                var $this = $(this);

                if ( $this.hasClass('selected') ) {
                    return false;
                }
                var $optionSet = $this.parents('.project_filters');
                    $optionSets.find('.selected').removeClass('selected');
                    $this.addClass('selected');

                var selector = $(this).attr('data-filter');
                    $container.isotope({ 
                        filter: selector 
                    });
                return false;
            });
        });
    };

    /* --------------------------------------------------
	* project carousel
	* --------------------------------------------------*/
    var portfolioSlider = function ( $scope , $ ) {
        $scope.find('.project-slider').each( function(){
            var $selector = $(this),
                $show   = $selector.data('show'),
                $scroll = $selector.data('scroll'),
                $arr    = $selector.data('arrow'),
                $dots   = $selector.data('dots'),
                $mshow  = $show,
                $marr   = $arr,
                $mdots  = $dots;
                if( $show == 4 ){ $mshow = $show - 1; }
                if( $(this).hasClass('arrow-s2') ){ $marr = false; $mdots = true; }
            $selector.not( '.slick-initialized' ).slick({
                rtl: rtl_slick(),
                slidesToShow: $show,
                slidesToScroll: $scroll,
                arrows: $arr,
                dots: $dots,
                autoplay: true,
                autoplaySpeed: 6000,
                adaptiveHeight: true,
                prevArrow: '<button type="button" class="prev-nav"><i class="flaticon-arrow-pointing-to-left"></i></button>',
                nextArrow: '<button type="button" class="next-nav"><i class="flaticon-arrow-pointing-to-right"></i></button>',
                responsive: [
                    {
                        breakpoint: 1199,
                        settings: {
                            slidesToShow: $mshow,
                            slidesToScroll: 1,
                            infinite: true,
                            arrows: $arr,
                            dots: $dots
                        }
                    },
                    {
                        breakpoint: 991,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1,
                            infinite: true,
                            arrows: $marr,
                            dots: $mdots
                        }
                    },
                    {
                        breakpoint: 600,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            arrows: false,
                            dots: true
                        }
                    }
                ]
            });
        } );
    };

    /* --------------------------------------------------
    * blog carousel
    * --------------------------------------------------*/
    var blogSlider = function ( $scope , $ ) {
        $scope.find('.onum-blog-slider').each( function(){
            var $selector = $(this),
                $show   = $selector.data('show'),
                $scroll = $selector.data('scroll'),
                $arr    = $selector.data('arrow'),
                $dots   = $selector.data('dots'),
                $mshow  = $show,
                $marr   = $arr,
                $mdots  = $dots;
                if( $show == 4 ){ $mshow = $show - 1; }
                if( $(this).hasClass('arrow-s2') ){ $marr = false; $mdots = true; }
            $selector.not( '.slick-initialized' ).slick({
                rtl: rtl_slick(),
                slidesToShow: $show,
                slidesToScroll: $scroll,
                arrows: $arr,
                dots: $dots,
                autoplay: true,
                autoplaySpeed: 6000,
                adaptiveHeight: true,
                prevArrow: '<button type="button" class="prev-nav"><i class="flaticon-arrow-pointing-to-left"></i></button>',
                nextArrow: '<button type="button" class="next-nav"><i class="flaticon-arrow-pointing-to-right"></i></button>',
                responsive: [
                    {
                        breakpoint: 1199,
                        settings: {
                            slidesToShow: $mshow,
                            slidesToScroll: 1,
                            infinite: true,
                            arrows: $arr,
                            dots: $dots
                        }
                    },
                    {
                        breakpoint: 991,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1,
                            infinite: true,
                            arrows: $marr,
                            dots: $mdots
                        }
                    },
                    {
                        breakpoint: 600,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            arrows: false,
                            dots: true
                        }
                    }
                ]
            });
        } );
    };

    /* --------------------------------------------------
    * social team
    * --------------------------------------------------*/
    var teamSocial = function ( $scope , $ ) {
        $scope.find('.team-social > span').on('click', function(){
            $(this).parent().toggleClass('active');
        });
    };

    /* --------------------------------------------------
	* team carousel
	* --------------------------------------------------*/
    var teamSlider = function ( $scope , $ ) {
        $scope.find('.team-social > span').on('click', function(){
            $(this).parent().toggleClass('active');
        });
        $scope.find('.team-slider').each( function(){
            var $selector = $(this),
                $show   = $selector.data('show'),
                $scroll = $selector.data('scroll'),
                $arr    = $selector.data('arrow'),
                $dots   = $selector.data('dots'),
                $tshow  = $show,
                $mshow  = $show,
                $marr   = $arr,
                $mdots  = $dots;
                if( $show == 5 ){ $tshow = 4; }
                if( $show >= 4 ){ $mshow = 3; }
                if( $(this).hasClass('arrow-s2') ){ $marr = false; $mdots = true; }
            $selector.not( '.slick-initialized' ).slick({
                rtl: rtl_slick(),
                slidesToShow: $show,
                slidesToScroll: $scroll,
                arrows: $arr,
                dots: $dots,
                infinite: false,
                autoplay: true,
                autoplaySpeed: 6000,
                adaptiveHeight: true,
                prevArrow: '<button type="button" class="prev-nav"><i class="flaticon-arrow-pointing-to-left"></i></button>',
                nextArrow: '<button type="button" class="next-nav"><i class="flaticon-arrow-pointing-to-right"></i></button>',
                responsive: [
                    {
                        breakpoint: 1499,
                        settings: {
                            slidesToShow: $tshow,
                            slidesToScroll: 1,
                            infinite: true,
                            arrows: $arr,
                            dots: $dots
                        }
                    },
                    {
                        breakpoint: 1199,
                        settings: {
                            slidesToShow: $mshow,
                            slidesToScroll: 1,
                            infinite: true,
                            arrows: $arr,
                            dots: $dots
                        }
                    },
                    {
                        breakpoint: 991,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1,
                            infinite: true,
                            arrows: $marr,
                            dots: $mdots
                        }
                    },
                    {
                        breakpoint: 600,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            arrows: false,
                            dots: true
                        }
                    }
                ]
            });
        } );
    };

    /* --------------------------------------------------
	* real numbers
	* --------------------------------------------------*/
	var realNumbers = function ( $scope , $ ) {
	    var swt = $('.real-numbers').find('.switch input');
	    swt.on( 'change', function() {
	        var parent = $(this).parents('.real-numbers');
	        if(this.checked) {
	            parent.find('.a-switch').addClass('active');
	            parent.find('.b-switch').removeClass('active');
	            parent.find('h2.after').fadeIn();
	            parent.find('h2.before').hide();
	        }else{
	            parent.find('.b-switch').addClass('active');
	            parent.find('.a-switch').removeClass('active');
	            parent.find('h2.after').hide();
	            parent.find('h2.before').fadeIn();
	        }
	    });
	};

	/* --------------------------------------------------
	* video popup
	* --------------------------------------------------*/
	var videoPopup = function () {
        var $video_play = $('.video-popup a');
        if ($video_play.length > 0 ) {
            $video_play.magnificPopup({
                type: 'iframe',
                removalDelay: 160,
                preloader: true,
                fixedContentPos: true,
                callbacks: {
                beforeOpen: function() {
                        this.st.image.markup = this.st.image.markup.replace('mfp-figure', 'mfp-figure mfp-with-anim');
                        this.st.mainClass = this.st.el.attr('data-effect');
                    }
                },
            });
        }
    };

    /* --------------------------------------------------
    * post grid isotope
    * --------------------------------------------------*/
    var postGrid = function ( $scope , $ ) {    
        $scope.find('.blog-grid').each( function(){
            var $container = $(this); 
            $container.isotope({ 
                itemSelector : '.masonry-post-item', 
                animationEngine : 'css',
            });
        });        
    };

    /* --------------------------------------------------
    * big tabs
    * --------------------------------------------------*/
    var tabTitles = function () {
        $('.tab-titles .title-item').on( 'click', function(){
            $('.tab-active').removeClass('tab-active');
            $(this).addClass('tab-active');
            $('#content-tabs .elementor-inner-section').removeClass('active');
            $('.content-tab-section').removeClass('active');
            $($(this).attr('href')).addClass('active');

            return false;
        });
        $('.tab-titles .title-item:first').trigger('click');
    };

    var tabSlider = function () {
        $('.tab-titles').each( function(){
            var $selector = $(this);
            $selector.not( '.slick-initialized' ).slick({
                rtl: rtl_slick(),
                slidesToShow: 6,
                slidesToScroll: 1,
                arrows: false,
                infinite: false,
                autoplay: false,
                adaptiveHeight: true,
                prevArrow: '<button type="button" class="prev-nav"><i class="flaticon-arrow-pointing-to-left"></i></button>',
                nextArrow: '<button type="button" class="next-nav"><i class="flaticon-arrow-pointing-to-right"></i></button>',
                responsive: [
                    {
                        breakpoint: 1199,
                        settings: {
                            slidesToShow: 5,
                            slidesToScroll: 1,
                            dots: true,
                        }
                    },
                    {
                        breakpoint: 991,
                        settings: {
                            slidesToShow: 4,
                            slidesToScroll: 1,
                            dots: true,
                        }
                    },
                    {
                        breakpoint: 767,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 1,
                            dots: true
                        }
                    },
                    {
                        breakpoint: 600,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1,
                            dots: true
                        }
                    },
                    {
                        breakpoint: 480,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            dots: true
                        }
                    }
                ]
            });
        } );
    };

    /* --------------------------------------------------
    * count down
    * --------------------------------------------------*/
    var countDown = function(){
        $('.ot-countdown').each( function() {
            var date   = $(this).data('date'),
                zone   = $(this).data('zone'),
                day    = $(this).data('day'),
                days   = $(this).data('days'),
                hour   = $(this).data('hour'),
                hours  = $(this).data('hours'),
                min    = $(this).data('min'),
                mins   = $(this).data('mins'),
                second = $(this).data('second'),
                seconds = $(this).data('seconds');
            $(this).countdown({
                date: date,
                offset: zone,
                day: day,
                days: days,
                hour: hour,
                hours: hours,
                minute: min,
                minutes: mins,
                second: second,
                seconds: seconds
            }, function () {
                alert('Done!');
            });
        });
    };

    /**
     * Elementor JS Hooks
     */
    $(window).on("elementor/frontend/init", function () {

    	/*counter*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/icounter.default",
            counter
        );

        /*progress bar + counter*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/iprogress.default",
            progressBar
        );

        /*custom tabs*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/itabs.default",
            customTabs
        );

        /*big tabs*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/itabtitle.default",
            tabTitles
        );

        /*title tabs slider*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/itabtitle.default",
            tabSlider
        );

        /*custom accordions*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/iaccordions.default",
            customAccordions
        );

        /*testimonials*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/itestimonials.default",
            testimonialSlider
        );

        /*message box*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/imessagebox.default",
            messageBox
        );

        /*real numbers*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/ichartnumber.default",
            realNumbers
        );

        /*video popup*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/ivideopopup.default",
            videoPopup
        );

        /*projects filter isotope*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/ipfilter.default",
            projectsFilter
        );

        /*projects carousel*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/irprojects.default",
            portfolioSlider
        );

        /*team carousel*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/iteams.default",
            teamSlider
        );

        /*team social*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/imember.default",
            teamSocial
        );

        /*post grid*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/ipost_grid.default",
            postGrid
        );

        /*blog carousel*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/ipost_carousel.default",
            blogSlider
        );

        /*countdown*/
        elementorFrontend.hooks.addAction(
            "frontend/element_ready/icountdown.default",
            countDown
        );
    });

} )( jQuery );