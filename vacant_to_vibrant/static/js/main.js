//
// main.js
//
// Scripts that should run on every page.
//

$(document).ready(function() {

    /*
     * Disable submit buttons on forms once they have been submitted once.
     */
    $('form').submit(function() {
        $(this).find('input[type="submit"]').attr('disabled', 'disabled');
    });

    /*
     * Fancybox
     */
    $('.fancybox').fancybox();

});
