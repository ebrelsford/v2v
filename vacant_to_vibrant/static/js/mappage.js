define(
    [
        // Dependencies we'll use the return values from
        'jquery',
        'leaflet',

        // Internal plugins
        'jquery.singleminded',
        'jquery.streetview',

        // Filter [de]serialization
        'lib/jquery.deserialize.min',
        'lib/jquery.serializeobject.min',

        // Leaflet Map mixin
        'leaflet.lotmap',

    ], function($, L) {

    function updateCounts() {
        var baseUrl = $('#map').data('mappagecountsbaseurl');
        $('#map').singleminded({
            name: 'counts',
            jqxhr: $.getJSON(baseUrl + $('form').serialize(), function(data) {
                $.each(data, function(label, count) {
                    $('.' + label).text(count);
                });
            }),
        });
    }

    function serializeFilters() {
        return $('form').serialize();
    }

    function deserializeFilters() {
        // Get filters from url query string
        var filters = window.location.search.slice(1);

        // Clear the form of any defaults, first
        if (filters.length > 1) {
            $(':checkbox').prop('checked', false);
        }

        // Drop filters into the form (which is spread over multiple forms)
        $('form').deserialize(filters);

        // Trigger Chosen to update selects
        $('select').trigger('liszt:updated');

        // Update map viewport
        var bboxString = $('#id_centroid__within').val();
        if (bboxString) {
            LOTS_MAP.fitBounds(L.geoJsonLatLngBounds(bboxString));
        }
    }

    var LOTS_MAP;
    $(document).ready(function() {
        var key = $('#map').data('cloudmadekey'),
            style = $('#map').data('cloudmadestyle');

        LOTS_MAP = L.map('map', {
            center: [39.952335, -75.163789],
            maxBounds: [
                [39.147, -76.358],
                [40.772, -73.952],
            ],
            zoom: 11,
            cloudmadeKey: key,
            cloudmadeStyleId: style,
            bingKey: 'ArBLp_jhvmrzT5Kg4_FXohJCKjbKmBW-nEEItp2dbceyHrJPMJJEqXDp8XsPy_cr',
            lotClickHandler: function(e, feature) {
                var popupOptions = {
                    minHeight: 250,
                    minWidth: 300,
                }
                var popupContent = '<div id="popup-content" class="loading"></div>';
                if (e.targetType == 'utfgrid') {
                    var popup = L.popup(popupOptions)
                        .setContent(popupContent)
                        .setLatLng(e.latlng)
                        .openOn(LOTS_MAP);
                }
                else {
                    e.target.bindPopup(popupContent, popupOptions).openPopup();
                }
                $.get('/places/lots/lot/' + feature.id + '/popup/', function(response) {
                    $('#popup-content')
                        .html(response)
                        .removeClass('loading');
                });
            },

            messageControl: true,
            messageDefault: 'Zoom in for details',

            enableLayersControl: true,

            enableLotChoropleth: true,
            lotChoroplethBaseUrl: $('#map').data('mappagelotchoroplethbaseurl'),
            lotChoroplethQueryString: 'parents_only=True',

            enableLotPolygons: true,
            lotPolygonBaseUrl: $('#map').data('mappagelotpolygonbaseurl'),
            lotPolygonInitialFilters: { 
                parentsOnly: true,
            },
        });

        deserializeFilters();

        updateCounts();

        LOTS_MAP.updateFilters($('form').serializeObject());
        LOTS_MAP.reloadLotCentroidLayer(serializeFilters());
        LOTS_MAP.reloadLotChoroplethLayer(serializeFilters());

        LOTS_MAP.on('moveend', function(e) {
            var g = JSON.stringify(LOTS_MAP.getBounds().toGeoJson())
            $(':input[name="centroid__within"]').val(
                JSON.stringify(LOTS_MAP.getBounds().toGeoJson())
            );
            updateCounts();
        });

        $('#streetview-container').streetview({
            errorSelector: '#streetview-error',
        });

        LOTS_MAP.on('lotclicked', function(data) {
            var event = data.event;
            $('#streetview-container').data('streetview').load_streetview(
                event.latlng.lng, event.latlng.lat);
        });

        LOTS_MAP.on('popupclose', function(e) {
            $('#streetview-container').hide();
        });

        $('.filters :input:not(.non-filter)').change(function() {
            updateCounts();
            LOTS_MAP.reloadLotCentroidLayer(serializeFilters());
            LOTS_MAP.reloadLotChoroplethLayer(serializeFilters());
            LOTS_MAP.updateFilters($('form').serializeObject());
        });

        $('.export-link').click(function() {
            // TODO make shorter urls
            window.location.search = serializeFilters();
        });

        $('.export-csv').click(function() {
            window.location = $(this).data('baseurl') + serializeFilters();
            return false;
        });

        $('.export-geojson').click(function() {
            window.location = $(this).data('baseurl') + serializeFilters();
            return false;
        });

        $('.export-kml').click(function() {
            window.location = $(this).data('baseurl') + serializeFilters();
            return false;
        });
    });

    return LOTS_MAP;
});
