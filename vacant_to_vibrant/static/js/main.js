//
// main.js
//
// Scripts that should run on every page.
//

define(['jquery'], function($) {

    /*
     * Global form-related scripts
     */
    $(document).ready(function() {
        /*
         * Disable submit buttons on forms once they have been submitted once.
         */
        $('form').submit(function() {
            $(this).find('input[type="submit"]').attr('disabled', 'disabled');
        });

        require(['lib/jquery.noisy'], function() {
            $('body').noisy({
                'intensity' : 1,
                'size' : 200,
                'opacity' : 0.08,
                'fallback' : '',
                'monochrome' : false
            }).css('background-color', '#61A194');
        });

        /*
         * Fancy the fancyboxes
         */
        require(['jquery', 'fancybox'], function() {
            $('.fancybox').fancybox();
        });
    });

    require(['chosen.jquery_ready']);


    /*
     * Page-specific modules
     */
    if ($('.lot-base-page').length > 0) {
        require(['lotbasepage']);
    }
    if ($('.add-organizer-page').length > 0) {
        require(['addorganizerpage']);
    }
    if ($('.home-map-page').length > 0) {
        require(['mappage']);
    }
    if ($('.extraadmin-mail-participants-page').length > 0) {
        require(['mailparticipantspage']);
    }

});
