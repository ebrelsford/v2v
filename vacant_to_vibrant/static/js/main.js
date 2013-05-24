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
     * TODO Split page-specific bits into their own build profiles or module
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

        require(['jquery.activitystream'], function() {
            $(document).ready(function() {
                $('.activity-stream-container').activitystream();
            });
        });

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

    if ($('.extraadmin-mail-participants-page').length > 0) {

        require(['jquery', 'django', 'mappage'], function($, Django, lotsMap) {
            function mail_participants_update_counts(with_bbox) {
                // TODO refactor urls to be outside of FeinCMS control
                var url = Django.url('extraadmin:mail_participants_count');
                    + $('form').serialize();
                $.getJSON(url, function(data) {
                    $('.organizer-count').text(data.organizers);
                    $('.watcher-count').text(data.watchers);
                });
            }

            $(document).ready(function() {

                lotsMap.on('moveend', function(e) {
                    var g = JSON.stringify(lotsMap.getBounds().toGeoJson())
                    $(':input[name="centroid__within"]').val(
                        JSON.stringify(lotsMap.getBounds().toGeoJson())
                    );
                    mail_participants_update_counts(true);
                });

                // initialize counts
                mail_participants_update_counts(false);

                $(':input').change(function() {
                    mail_participants_update_counts(true);

                    if ($(':input[name="participant_types"]:checked').length > 0) {
                        lotsMap.reloadLotCentroidLayer($('form').serialize());
                    }
                    else {
                        // if there aren't any participant types selected,
                        // don't show anything--no emails will go out
                        lotsMap.clearLotCentroidLayer();
                    }
                });

            });
        });
            
    }

});
