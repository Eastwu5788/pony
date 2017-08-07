/**
 * Created by Administrator on 2017/8/1.
 */

window.onload = function(){
    var mySwiper = new Swiper('.swiper-container',{

        speed:400,
	    // mode : 'vertical',
        direction: 'vertical',
	    resistance:'100%',

        // loop:true,
	    mousewheelControl : true,
	    grabCursor: true,

	    pagination: '.swiper-pagination',
        paginationClickable: true,

        onInit: function () {
            $('.slide1').addClass('ani-slide');
        }

        // onFirstInit:function(){
		 //    $('.slide1').addClass('ani-slide');
        // }
    });


    mySwiper.wrapper.transitionEnd(function () {//隐藏方法
	    $('.ani-slide').removeClass('ani-slide');
	    $('.swiper-slide').eq(mySwiper.activeIndex).addClass('ani-slide');
	}, true);
};