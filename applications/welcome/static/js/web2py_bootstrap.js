// this code improves bootstrap menus and adds dropdown support
jQuery(function(){
  jQuery('.nav>li>a').each(function(){
    if(jQuery(this).parent().find('ul').length)
      jQuery(this).attr({'class':'dropdown-toggle','data-toggle':'dropdown'}).append('<b class="caret"></b>');
  });
  jQuery('.nav li li').each(function(){
    if(jQuery(this).find('ul').length)
      jQuery(this).addClass('dropdown-submenu');
  });
  function hoverMenu(){
<<<<<<< HEAD
    var wid = document.documentElement.clientWidth; //faster than $(window).width() and cross browser
    if (wid>=980){
        jQuery('ul.nav a.dropdown-toggle').parent().hover(function(){
            mi = jQuery(this).addClass('open');
            mi.children('.dropdown-menu').stop(true, true).delay(200).fadeIn(400);
        }, function(){
            mi = jQuery(this);
            mi.children('.dropdown-menu').stop(true, true).delay(200).fadeOut(function(){mi.removeClass('open')});
        });
    };
=======
    jQuery('ul.nav a.dropdown-toggle').parent().hover(function(){
        adjust_height_of_collapsed_nav();
        var mi = jQuery(this).addClass('open');
        mi.children('.dropdown-menu').stop(true, true).delay(200).fadeIn(400);
    }, function(){
        var mi = jQuery(this);
        mi.children('.dropdown-menu').stop(true, true).delay(200).fadeOut(function(){mi.removeClass('open')});
    });
>>>>>>> 4cbdf612af9e9c992e99c6c9e60e2170e4deb853
  }
  hoverMenu(); // first page load
  jQuery(window).resize(hoverMenu); // on resize event
  jQuery('ul.nav li.dropdown a').click(function(){window.location=jQuery(this).attr('href');});
<<<<<<< HEAD
  // make all buttons bootstrap buttons
  jQuery('button, form input[type="submit"], form input[type="button"]').addClass('btn');
=======
>>>>>>> 4cbdf612af9e9c992e99c6c9e60e2170e4deb853
});
