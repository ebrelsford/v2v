define(['jquery', 'django', 'mappage'], function($, Django, lotsMap) {

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
