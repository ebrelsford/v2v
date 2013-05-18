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

    var lotsMap;


    /*
     * Update counts
     */
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


    /*
     * Handle filter inputs
     */
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
            lotsMap.fitBounds(L.geoJsonLatLngBounds(bboxString));
        }
    }

    function onFilterChange() {
        updateCounts();
        lotsMap.updateFilters($('form').serializeObject());
    }

    $(document).ready(function() {
        var key = $('#map').data('cloudmadekey'),
            style = $('#map').data('cloudmadestyle');


        // Prepare our map
        lotsMap = L.map('map', {
            center: [39.952335, -75.163789],
            maxBounds: [
                [39.147, -76.358],
                [40.772, -73.952],
            ],
            zoom: 11,
            cloudmadeKey: key,
            cloudmadeStyleId: style,
            bingKey: 'ArBLp_jhvmrzT5Kg4_FXohJCKjbKmBW-nEEItp2dbceyHrJPMJJEqXDp8XsPy_cr',
            clickHandler: function(e, feature) {
                var featureId = null;
                if (feature) featureId = feature.id;
                var popupOptions = {
                    minHeight: 250,
                    minWidth: 300,
                }
                var popupContent = '<div id="popup-content" class="loading"></div>';
                if (e.targetType === 'utfgrid' && e.data !== null) {
                    featureId = e.data.id;
                    var popup = L.popup(popupOptions)
                        .setContent(popupContent)
                        .setLatLng(e.latlng)
                        .openOn(lotsMap);
                }
                else {
                    try {
                        e.target.bindPopup(popupContent, popupOptions).openPopup();
                    }
                    catch (e) {}
                }
                // TODO get url dynamically
                if (featureId !== null) {
                    $('#map').singleminded({
                        name: 'clickHandler',
                        jqxhr: $.get('/places/lots/lot/' + featureId + '/popup/', function(response) {
                            $('#popup-content')
                                .html(response)
                                .removeClass('loading');
                        }),
                    });
                }
            },

            messageControl: true,
            messageDefault: 'Zoom in for details',

            enableLayersControl: true,

            enableChoropleth: true,
            choroplethBaseUrl: $('#map').data('mappagechoroplethbaseurl'),
            choroplethQueryString: 'parents_only=True',

            enablePolygons: true,
            polygonBaseUrl: $('#map').data('mappagepolygonbaseurl'),
            polygonInitialFilters: { 
                parentsOnly: true,
            },

            gridResolution: 8,

            enablePointPrivateTiles: true,
            pointPrivateTilesBaseUrl: $('#map').data('mappagepointprivatetilesbaseurl'),
            pointPrivateGridBaseUrl: $('#map').data('mappagepointprivategridbaseurl'),

            enablePointPublicTiles: true,
            pointPublicTilesBaseUrl: $('#map').data('mappagepointpublictilesbaseurl'),
            pointPublicGridBaseUrl: $('#map').data('mappagepointpublicgridbaseurl'),

        });

        // Load filters from search string in URL, update map/counts accordingly
        deserializeFilters();
        onFilterChange();


        /*
         * Map events
         */
        lotsMap.on('moveend', function(e) {
            var g = JSON.stringify(lotsMap.getBounds().toGeoJson())
            $(':input[name="centroid__within"]').val(
                JSON.stringify(lotsMap.getBounds().toGeoJson())
            );
            updateCounts();
        });

        lotsMap.on('lotclicked', function(data) {
            var event = data.event;
            $('#streetview-container').data('streetview').load_streetview(
                event.latlng.lng, event.latlng.lat);
        });

        lotsMap.on('popupclose', function(e) {
            $('#streetview-container').hide();
        });


        /*
         * Filters events
         */
        $('.filters :input:not(.non-filter)').change(onFilterChange);


        /*
         * Prepare streetview
         */
        $('#streetview-container').streetview({
            errorSelector: '#streetview-error',
        });


        /*
         * Handle export actions
         */
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

    return lotsMap;
});
