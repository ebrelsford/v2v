define(['jquery', 'leaflet', 'jquery.streetview'], function($, L) {
    $(document).ready(function() {
        $streetviewContainer = $('#streetview-container');
        $streetviewContainer.streetview({
            errorSelector: '#streetview-error',
        });
        $streetviewContainer.data('streetview').load_streetview(
            $streetviewContainer.data('lon'),
            $streetviewContainer.data('lat')
        );
    });

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

    var feature_layer = new L.GeoJSON(null, {

        pointToLayer: function(data, latlng) {
            return new L.marker(latlng);
        },

        style: function(feature) {
            return {
                radius: 1,
                fillColor: "#000000",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8,
            }
        },

    });

    $.get($('#map').data('url'), function(collection) {
        feature_layer.addData(collection);
        map.addLayer(feature_layer);
        map.fitBounds(feature_layer.getBounds());
    });

});
