define(
    [
        // Dependencies we'll use the return values from
        'jquery',
        'leaflet',
        'django',
        'json2',

        // Internal plugins
        'jquery.emailparticipants',
        'jquery.searchbar',
        'jquery.singleminded',
        'jquery.streetview',

        // Filter [de]serialization
        'lib/jquery.deserialize.min',
        'lib/jquery.serializeobject.min',

        // Leaflet Map mixin
        'leaflet.lotmap',

        'jqueryui',
        'lib/jquery.spin',
        'lib/jquery.smartresize',

        'lib/leaflet.usermarker/leaflet.usermarker',

    ], function ($, L, Django, JSON) {

        var MAX_LOTS_DOWNLOAD = 2000;

        var currentViewType,
            lotsMap,
            mapViewportSet = false,
            visibleLotsCount = 0;


        /*
         * Get bounds for searching
         */
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


        /*
         * Update counts
         */
        function updateCounts() {
            lotsMap.fire('dataloading');
            var baseUrl = $('#map').data('countsbaseurl');
            $('#map').singleminded({
                name: 'counts',
                jqxhr: $.getJSON(baseUrl + $('form').serialize(), function (data) {
                    $.each(data, function (label, count) {
                        $('.' + label).text(count);
                    });
                    visibleLotsCount = data['lots-count'];
                    lotsMap.setVisibleLotsCount(visibleLotsCount);
                })
                .always(function () {
                    lotsMap.fire('dataload');
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
            var bboxString = $(':input[name="centroid__within"]').val();
            if (bboxString) {
                mapViewportSet = true;
                lotsMap.fitBounds(L.geoJsonLatLngBounds(bboxString));
            }
            var zoomString = $(':input[name="zoom"]').val();
            var zoom = 16;
            if (zoomString) {
                zoom = parseInt(zoomString, 10);
            }
            var centroidString = $(':input[name="centroid"]').val();
            if (centroidString) {
                mapViewportSet = true;
                // TODO This works, but doesn't seem to make the lotlayer load?
                lotsMap.setView(JSON.parse(centroidString), zoom);
            }
        }

        function exportView() {
            if (visibleLotsCount > MAX_LOTS_DOWNLOAD) {
                alert('Too many lots to download! Filter the map and try again once the number of lots is no more than ' + MAX_LOTS_DOWNLOAD + '.');
            }
            else {
                window.location = $(this).data('baseurl') + serializeFilters();
            }
            return false;
        }

        function updateViewType(viewType) {
            currentViewType = viewType;
            var viewTypeFilterSelector = '.view-type-' + viewType;

            // {En,Dis}able filters that should be {en,dis}abled for this view type
            $('.filter :input').prop('disabled', function (i, value) {
                return !$(this).parents('.filter').is(viewTypeFilterSelector);
            });

            // Hide filters that have been disabled, show those enabled
            $('.filter' + viewTypeFilterSelector).removeClass('is-disabled');
            $('.filter:not(' + viewTypeFilterSelector + ')').addClass('is-disabled');

            // Hide/Show filter labels if there are any filters enabled below
            // them
            $('.map-filters h2:not(.always-enabled)').each(function () {
                if ($(this).nextAll().find('.filter:not(.is-disabled)').length > 0) {
                    $(this).show();
                }
                else {
                    $(this).hide();
                }
            });

            // Always enable default filters (for counts)
            $('.filter.default :input').prop('disabled', false);

            // TODO for viewType===tiles, reset filters that are disabled 
            //  (ensures sanity and that counts are appropriate)
        }

        function onFilterChange() {
            if ($(this).attr('name') === 'view_type') {
                updateViewType($(this).val());
            }
            updateCounts();
            var serializedFilters = $('.filters :input:not(.non-filter)').serializeObject();
            lotsMap.updateFilters(serializedFilters);
            lotsMap.fire('filterschange', { filters: serializedFilters, });
        }

        function showOverlay() {
            $('#map-overlay').show();
            positionOverlay();
        }

        function positionOverlay() {
            $('#map-overlay').position({
                my: 'center center',
                at: 'center center',
                of: $('#map'),
            });
        }

        function hideOverlay() {
            $('#map-overlay').hide();
        }

        $(document).ready(function () {
            var mapboxId = $('#map').data('mapboxid');

            // Prepare our map
            lotsMap = L.map('map', {
                center: [39.952335, -75.163789],
                maxBounds: [
                    [39.147, -76.358],
                    [40.772, -73.952],
                ],
                zoom: 11,
                mapboxId: mapboxId,
                bingKey: 'ArBLp_jhvmrzT5Kg4_FXohJCKjbKmBW-nEEItp2dbceyHrJPMJJEqXDp8XsPy_cr',
                clickHandler: function (e, feature) {
                    var featureId = null;
                    if (feature) featureId = feature.id;
                    var popupOptions = {
                        maxHeight: 150
                    };
                    if (L.Browser.mobile === true) {
                        popupOptions.maxWidth = 200;
                        popupOptions.minWidth = 200;
                    }
                    else {
                        popupOptions.minWidth = 300;
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
                    var url = Django.url('inplace:lots_lot_detail_popup', { pk: featureId });
                    if (featureId !== null) {
                        $('#map').singleminded({
                            name: 'clickHandler',
                            jqxhr: $.get(url, function (response) {
                                $('#popup-content')
                                    .html(response)
                                    .removeClass('loading')
                                    .spin(false);
                            }),
                        });
                    }
                },

                messageControl: true,
                messageDefault: 'Zoom in for details',

                legendControl: true,
                legendFeatureTypes: [
                    { name: 'public', },
                    { name: 'private', },
                    { name: 'in use', },
                ],

                loadingControl: true,

                enableLayersControl: true,

                enableChoropleth: true,
                choroplethBaseUrl: $('#map').data('choroplethbaseurl'),
                choroplethQueryString: 'parents_only=True',

                enablePolygons: true,
                polygonBaseUrl: $('#map').data('polygonbaseurl'),
                polygonInitialFilters: {
                    parentsOnly: true,
                },

                enableCentroids: true,
                centroidBaseUrl: $('#map').data('centroidbaseurl'),
                centroidInitialFilters: {
                    parentsOnly: true,
                },

                lotsCentroidThreshold: 2000,

                gridResolution: 8,

                enablePointPrivateTiles: true,
                pointPrivateTilesBaseUrl: $('#map').data('pointprivatetilesbaseurl'),
                pointPrivateGridBaseUrl: $('#map').data('pointprivategridbaseurl'),

                enablePointPublicTiles: true,
                pointPublicTilesBaseUrl: $('#map').data('pointpublictilesbaseurl'),
                pointPublicGridBaseUrl: $('#map').data('pointpublicgridbaseurl'),

                enablePointInUseTiles: true,
                pointInUseTilesBaseUrl: $('#map').data('pointinusetilesbaseurl'),
                pointInUseGridBaseUrl: $('#map').data('pointinusegridbaseurl'),

            });

            /*
             * Map events
             */
            lotsMap.on('moveend', function (e) {
                var g = JSON.stringify(lotsMap.getBounds().toGeoJson());
                $(':input[name="centroid__within"]').val(
                    JSON.stringify(lotsMap.getBounds().toGeoJson())
                );
                $(':input[name="centroid"]').val(
                    JSON.stringify(lotsMap.getCenter())
                );
                $(':input[name="zoom"]').val(lotsMap.getZoom());

                updateCounts();
                var serializedFilters = $('.filters :input:not(.non-filter)').serializeObject();
                lotsMap.fire('filterschange', { filters: serializedFilters, });
            });

            lotsMap.on('lotclicked', function (data) {
                var event = data.event;
                $('#streetview-container').data('streetview').load_streetview(
                    event.latlng.lng, event.latlng.lat);
            });

            lotsMap.on('popupopen', function (e) {
                $('#popup-content.loading').spin('large');
                lotsMap.messageControl.hide();
            });

            lotsMap.on('popupclose', function (e) {
                $('#streetview-container').hide();
            });

            lotsMap.whenReady(function (e) {
                // Load filters from search string in URL, update map/counts accordingly
                deserializeFilters();
                onFilterChange();

                // Update map and UI with the current view
                var currentView = $(':input[name=view_type]').val();
                updateViewType(currentView);
                lotsMap.changeView(currentView);
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
            $('.export-link').click(function () {
                // TODO make shorter urls
                window.location.search = serializeFilters();
            });

            $('.export-csv').click(exportView);
            $('.export-geojson').click(exportView);
            $('.export-kml').click(exportView);


            // Fire up the emailparticipants
            $('.email-participants').emailparticipants({
                filterContainer: lotsMap,
            });


            // Fire up searchbar
            $('.searchbar')
                .searchbar({
                    bounds: getBounds(lotsMap),
                    city: 'Philadelphia',
                    state: 'PA',
                    errorMessage: "Sorry, it doesn't seem that the address you " +
                        "entered is in Philadelphia. Try again?",
                    warningSelector: '.warning',
                })
                .on('searchresultfound', function (e, data) {
                    hideOverlay();
                    var latlng = [data.latitude, data.longitude];
                    lotsMap.setView(latlng, 18);
                    var usermarker = L.userMarker(latlng, { smallIcon: true })
                        .bindPopup('This is the address you searched for.');
                    usermarker.addTo(lotsMap);
                });


            // Show/hide filters
            $('.map-filters-toggle').click(function () {
                $('.map-filters').toggle();
            });

            // Overlay
            if (!mapViewportSet) {
                showOverlay();
                $(window).smartresize(positionOverlay);
                $('.map-overlay-button').click(hideOverlay);
                $('.map-overlay-close-button').click(hideOverlay);
            }

        });

        return lotsMap;
    }
);
