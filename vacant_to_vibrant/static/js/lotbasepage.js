/*
 * Module for all pages derived from the base lot page.
 */
define(
    [
        'jquery',
        'leaflet',
        'jquery.streetview',
        'lib/bootstrap/bootstrap-tooltip'
    ], function($, L) {

    $(document).ready(function() {
        $streetviewContainer = $('#streetview-container');
        $streetviewContainer.streetview({
            errorSelector: '#streetview-error',
        });
        $streetviewContainer.data('streetview').load_streetview(
            $streetviewContainer.data('lon'),
            $streetviewContainer.data('lat')
        );

        var map = new L.Map('map');
        var key = $('#map').data('cloudmadekey'),
            style = $('#map').data('cloudmadestyle');
        var cloudmade = new L.TileLayer(
            'http://{s}.tile.cloudmade.com/' + key + '/' + style +'/256/{z}/{x}/{y}.png', 
            {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
                maxZoom: 18,
            }
        );
        map.addLayer(cloudmade);

        $.get($('#map').data('url'), function(data) {
            var style = {
                fillColor: 'hsl(140, 42%, 40%)',
                fillOpacity: .7,
                color: 'white',
                opacity: .8,
                weight: 2,
            };
            var feature_layer = new L.GeoJSON(data, { style: style, }).addTo(map);
            map.fitBounds(feature_layer.getBounds());
        });

        $('.build-community-button').tooltip();

    });

});
