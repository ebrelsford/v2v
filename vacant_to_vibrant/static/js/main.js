//
// main.js
//
// Scripts that should run on every page.
//

define(
    [
        'jquery',

        'jquery.activitystream',
        'lib/bootstrap/bootstrap-dropdown'
    ], function ($) {

        /*
        * Global form-related scripts
        */
        $(document).ready(function () {
            /*
            * Disable submit buttons on forms once they have been submitted once.
            */
            $('form').submit(function () {
                $(this).find('input[type="submit"]').attr('disabled', 'disabled');
            });

            require(['lib/jquery.noisy'], function () {
                $('body').noisy({
                    'intensity' : 0.5,
                    'size' : 100,
                    'opacity' : 0.15,
                    'fallback' : '',
                    'monochrome' : false
                });
            });

            /*
            * Collapse the collapsible sections
            */
            require(['jquery'], function () {
                // Slide up those sections not initially expanded
                $('.collapsible-section:not(.is-expanded) .collapsible-section-text').slideUp();

                // Prepare headers for clicking
                $('.collapsible-section-header').click(function () {
                    var $section = $(this).parent(),
                        $sectionText = $section.find('.collapsible-section-text');
                    $section.toggleClass('is-expanded');
                    $sectionText.slideToggle();
                });
            });

            /*
            * Fancy the fancyboxes
            */
            require(['jquery', 'fancybox'], function () {
                $('.fancybox').fancybox();
            });

            /*
            * Activate the activitystreams
            */
            require(['jquery.activitystream'], function () {
                $('.activity-stream-container').activitystream();
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
