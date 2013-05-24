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
    });

    require(['chosen.jquery_ready']);


    /*
     * Page-specific modules
     */
    if ($('.lot-base-page').length > 0) {
        require(['lotbasepage']);
    }
    if ($('.lot-detail-page').length > 0) {
        require(['lotdetailpage']);
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
