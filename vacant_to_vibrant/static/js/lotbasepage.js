/*
 * Module for all pages derived from the base lot page.
 */
define(
    [
        'jquery',
        'leaflet',
        'lotstyles',

        'jquery.streetview',
        'lib/bootstrap/bootstrap-tooltip'
    ], function ($, L, lotStyles) {

        function styleLayer(feature) {
            return lotStyles[feature.properties.layer];
        }

        $(document).ready(function () {
            var $streetviewContainer = $('#streetview-container'),
                lon = $('body').data('lon'),
                lat = $('body').data('lat');

            // Set up streetview
            $streetviewContainer.streetview({
                errorSelector: '#streetview-error',
            });
            $streetviewContainer.data('streetview').load_streetview(lon, lat);

            // Set up lot map
            var map = new L.Map('map', {
                center: { lat: lat, lng: lon },
                zoom: 17
            });
            var key = $('#map').data('cloudmadekey'),
                style = $('#map').data('cloudmadestyle');
            var cloudmade = new L.TileLayer(
                'http://{s}.tile.cloudmade.com/' + key + '/' + style + '/256/{z}/{x}/{y}.png',
                {
                    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
                    maxZoom: 18,
                }
            );
            map.addLayer(cloudmade);

            $.get($('#map').data('url'), function (data) {
                var feature_layer = new L.GeoJSON(data, { style: styleLayer })
                    .addTo(map);
            });

            $('.lot-page-tooltip').tooltip({ container: 'body' });

        });

    }
);
