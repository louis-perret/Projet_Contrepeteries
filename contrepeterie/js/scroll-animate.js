$(document).ready(function() {
    $('body').on('click', '.navbar-nav li a', function(e) {
        $('a.active').removeClass('active');
        var link = $(this);
        //link.closest('a').addClass('active');
        // Scroll animation
        $('html, body').animate( { scrollTop: $(link.attr('href')).offset().top }, 750 );
        return false;
    });

    //Scrollspy
    $('body').scrollspy({ target: '#nvbar' });
});