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

        var lotPk;

        function styleLayer(feature) {
            var style = lotStyles[feature.properties.layer];
            if (+feature.properties.pk !== lotPk) {
                style.fillOpacity = 0.3;
                style.weight = 0.5;
            }
            else {
                style.fillOpacity = 1;
                style.weight = 3;
            }
            return style;
        }

        $(document).ready(function () {
            var $streetviewContainer = $('#streetview-container'),
                lon = $('body').data('lon'),
                lat = $('body').data('lat');

            lotPk = $('body').data('lotpk');

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
            L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                mapboxId: $('#map').data('mapboxid')
            }).addTo(map);

            $.get($('#map').data('url'), function (data) {
                var feature_layer = new L.GeoJSON(data, { style: styleLayer })
                    .addTo(map);
            });

            $('.lot-page-tooltip').tooltip({ container: 'body' });

        });

    }
);
