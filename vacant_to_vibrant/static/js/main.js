//
// main.js
//
// Scripts that should run on every page.
//

define(['jquery'], function($) {

    $(document).ready(function() {
        /*
        * Disable submit buttons on forms once they have been submitted once.
        */
        $('form').submit(function() {
            $(this).find('input[type="submit"]').attr('disabled', 'disabled');
        });
    });

    require(['jquery.activitystream'], function() {
        $(document).ready(function() {
            $('.activity-stream-container').activitystream();
        });
    });

    require(['chosen.jquery_ready']);

    if ($('.lot-detail-page').length > 0) {
        require(['lotdetailpage']);

        require(['fancybox'], function() {
            $(document).ready(function() {
                $('.fancybox').fancybox();
            });
        });
    }

    if ($('.home-map-page').length > 0) {
        require(['mappage', 'jquery.searchbar',], function(LOTS_MAP) {

            function getBounds(map) {
                var bounds = map.options.maxBounds;
                var seBounds = bounds.getSouthEast();
                var nwBounds = bounds.getNorthWest();

                return [
                    seBounds.lng,
                    seBounds.lat,
                    nwBounds.lng,
                    nwBounds.lat
                ];
            }

            $(document).ready(function() {
                $('.searchbar')
                    .searchbar({
                        bounds: getBounds(LOTS_MAP),
                        city: 'Philadelphia',
                        state: 'PA',
                        errorMessage: "Sorry, it doesn't seem that the address you " +
                            "entered is in Philadelphia. Try again?",
                        loadingSelector: '.loading',
                        warningSelector: '.warning',
                    })
                    .on('searchresultfound', function(e, data) {
                        LOTS_MAP.setView([data.latitude, data.longitude], 15);
                    });
            });
        });

        require(['mappage']);
    }
});
