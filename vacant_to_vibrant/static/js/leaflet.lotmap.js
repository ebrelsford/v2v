/*
 * L.LotMap -- mixin for L.Map that adds layers for vacant to vibrant.
 */

define(
    [
        // Dependencies we'll use the return values from
        'jquery',
        'leaflet',
        'lib/leaflet.lvector',
        'django',
        'underscore',
        'lotstyles',

        // Leaflet plugins
        'lib/leaflet.label',
        'lib/leaflet.utfgrid',
        'Leaflet.Bing',
        'leaflet.geojsonbounds',
        'leaflet.lotlayer',
        'leaflet.message',
        'leaflet.legend',
        'Control.Loading',

        // Other plugins
        'jquery.singleminded',

    ], function ($, L, lvector, Django, _, lotStyles) {

        L.Map.include({

            /*
            options: {
                bingKey: String,
                centroidBaseUrl: String,
                centroidInitialFilters: Object,
                enableLayersControl: Boolean,
                enableChoropleth: Boolean,
                enablePointTiles: Boolean,
                enablePolygons: Boolean,
                polygonBaseUrl: String,
                polygonInitialFilters: Object,
                mapboxId: String,
                messageControl: Boolean,
                messageDefault: String,
                lotsCentroidThreshold: Integer,
            },
            */

            choroplethHsl: {
                hue: 140,
                saturation: 42,
                lightness: 90,
            },

            choroplethStyle: {
                fillOpacity: 0.7,
                color: 'white',
                opacity: 0.8,
                weight: 2,
            },

            tileLayers: {
                'public': [],
                'private': [],
                'not in use': [],
                'in use': [],
            },

            choroplethBoundaryLayerName: null,
            filters: {},
            viewType: 'tiles',
            visibleLotsCount: 0,


            _lotMapInitialize: function () {
                // Add base layers
                this.addSatelliteLayer(false);
                this.addStreetsLayer();

                // Add overlays
                this.addCentroidLayer();
                this.addChoroplethLayer();
                this.addPolygonLayer();
                this.addTilesLayers();

                // Add controls
                this.addLayersControl();

                // Add events
                this.addZoomEvents();
            },


            /*
            * Base layers
            */

            addStreetsLayer: function () {
                this.streets = L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
                    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
                    maxZoom: 18,
                    mapboxId: this.options.mapboxId
                }).addTo(this);
            },

            addSatelliteLayer: function (add) {
                this.satellite = new L.BingLayer(this.options.bingKey);
                if (add) this.satellite.addTo(this);
            },


            /*
            * Overlay layers
            */


            /*
            * Tiles layers
            */

            addTilesLayers: function () {
                this.addPointPrivateTilesLayer();
                this.addPointPrivateGridLayer();
                this.addPointPublicTilesLayer();
                this.addPointPublicGridLayer();
                this.addPointInUseTilesLayer();
                this.addPointInUseGridLayer();
            },

            addGridLayer: function (baseUrl) {
                if (!baseUrl) return;
                var instance = this;
                var url = baseUrl + '{z}/{x}/{y}.json?callback={cb}';
                var gridLayer = new L.UtfGrid(url, {
                    resolution: this.options.gridResolution,
                });
                if (instance.options.clickHandler) {
                    gridLayer.on('click', function (e) {
                        e.targetType = 'utfgrid';
                        instance.options.clickHandler(e);
                    });
                }
                instance.addLayer(gridLayer);
                return gridLayer;
            },

            addPointPrivateTilesLayer: function () {
                if (!(this.options.enablePointPrivateTiles && this.viewType === 'tiles')) return;
                if (!this.options.pointPrivateTilesBaseUrl) return;

                var url = this.options.pointPrivateTilesBaseUrl + '{z}/{x}/{y}.png';
                this.tilesPointPrivate = L.tileLayer(url, {
                    zIndex: 10,
                    // TODO maxZoom
                }).addTo(this);
                this.tileLayers['private'].push(this.tilesPointPrivate);
                this.tileLayers['not in use'].push(this.tilesPointPrivate);
            },

            addPointPrivateGridLayer: function () {
                if (!(this.options.enablePointPrivateTiles && this.viewType === 'tiles')) return;
                this.gridPointPrivate = this.addGridLayer(this.options.pointPrivateGridBaseUrl);
                this.tileLayers['private'].push(this.gridPointPrivate);
                this.tileLayers['not in use'].push(this.gridPointPrivate);
                this.addLayer(this.gridPointPrivate);
            },

            addPointPublicTilesLayer: function () {
                if (!(this.options.enablePointPublicTiles && this.viewType === 'tiles')) return;
                if (!this.options.pointPublicTilesBaseUrl) return;

                var url = this.options.pointPublicTilesBaseUrl + '{z}/{x}/{y}.png';
                this.tilesPointPublic = L.tileLayer(url, {
                    zIndex: 12,
                    // TODO maxZoom
                }).addTo(this);
                this.tileLayers['public'].push(this.tilesPointPublic);
                this.tileLayers['not in use'].push(this.tilesPointPublic);
            },

            addPointPublicGridLayer: function () {
                if (!(this.options.enablePointPublicTiles && this.viewType === 'tiles')) return;
                this.gridPointPublic = this.addGridLayer(this.options.pointPublicGridBaseUrl);
                this.tileLayers['public'].push(this.gridPointPublic);
                this.tileLayers['not in use'].push(this.gridPointPublic);
            },

            addPointInUseTilesLayer: function () {
                if (!(this.options.enablePointInUseTiles && this.viewType === 'tiles')) return;
                if (!this.options.pointInUseTilesBaseUrl) return;

                var url = this.options.pointInUseTilesBaseUrl + '{z}/{x}/{y}.png';
                this.tilesPointInUse = L.tileLayer(url, {
                    zIndex: 14,
                    // TODO maxZoom
                }).addTo(this);
                this.tileLayers['in use'].push(this.tilesPointInUse);
            },

            addPointInUseGridLayer: function () {
                if (!(this.options.enablePointInUseTiles && this.viewType === 'tiles')) return;
                this.gridPointInUse = this.addGridLayer(this.options.pointInUseGridBaseUrl);
                this.tileLayers['in use'].push(this.gridPointInUse);
            },

            showTiles: function () {
                var instance = this;
                if (instance.viewType !== 'tiles') return;
                var filtered = _.size(instance.filters) > 0;
                var activeOwnerTypes = instance.getActiveOwnerTypes(instance.filters);
                var activeKnownUseExistences = instance.getActiveKnownUseExistence(instance.filters);
                var activeLayers = _.union(activeOwnerTypes, activeKnownUseExistences);

                _.each(_.keys(instance.tileLayers), function (layer) {
                    if (!filtered) {
                        // Always show if there are no current filters
                        instance.showTilesByLayer(layer);
                    }
                    else {
                        if (_.contains(activeKnownUseExistences, 'not in use')) {
                            // If 'not in use' is selected, show activeOwnerTypes
                            // and 'in use' if it is selected
                            if (layer === 'not in use') {
                                return;
                            }
                            else if (layer === 'in use' && _.contains(activeKnownUseExistences, layer)) {
                                instance.showTilesByLayer(layer);
                            }
                            else if (_.contains(activeOwnerTypes, layer)) {
                                instance.showTilesByLayer(layer);
                            }
                            else {
                                instance.hideTilesByLayer(layer);
                            }
                        }
                        else {
                            // If 'not in use' is *not* selected, do not show any 
                            // layers except those representing other known use
                            // existences
                            if (_.contains(activeKnownUseExistences, layer)) {
                                instance.showTilesByLayer(layer);
                            }
                            else {
                                instance.hideTilesByLayer(layer);
                            }
                        }
                    }
                });
            },

            hideTiles: function () {
                var instance = this;
                _.each(_.keys(instance.tileLayers), function (layer) {
                    instance.hideTilesByLayer(layer);
                });
            },

            showTilesByLayer: function (name) {
                var instance = this;
                _.each(instance.tileLayers[name], function (layer) {
                    if (layer) {
                        instance.addLayer(layer);
                    }
                });
            },

            hideTilesByLayer: function (name) {
                var instance = this;
                _.each(instance.tileLayers[name], function (layer) {
                    if (layer) {
                        instance.removeLayer(layer);
                    }
                });
            },

            getActiveOwnerTypes: function (filters) {
                var activeOwnerTypes = filters['owner__owner_type__in'];
                if (!activeOwnerTypes) {
                    return [];
                }
                else if (!_.isArray(activeOwnerTypes)) {
                    return [activeOwnerTypes,];
                }
                return activeOwnerTypes;
            },

            getActiveKnownUseExistence: function (filters) {
                var existence = filters['known_use_existence'];
                if (!existence) {
                    return [];
                }
                else if (!_.isArray(existence)) {
                    return [existence,];
                }
                return existence;
            },

            /*
            * Update which tiles are shown by owner type
            */
            reloadTiles: function (filters) {
                var instance = this;
                instance.filters = filters;
                instance.showTiles();
            },


            /*
            * Polygons
            */

            addPolygonLayer: function (queryString) {
                if (!queryString) {
                    queryString = this.options.polygonQueryString;
                }
                this._loadPolygonLayer(queryString, true);
            },

            addToPolygonLayer: function (queryString) {
                this._loadPolygonLayer(queryString, false);
            },

            reloadPolygonLayer: function (filters) {
                if (this.polygons === undefined) return;
                this.polygons._clearFeatures();
                this.polygons._lastQueriedBounds = null;
                this.polygons.options.filters = filters;
                this.polygons._getFeatures();
            },

            _getPolygonLayer: function () {
                var instance = this;
                var symbologyValues = _.map(lotStyles, function (style, name) {
                    return {
                        value: name,
                        vectorOptions: style
                    };
                });

                return new lvector.LotLayer({
                    map: instance,
                    clickEvent: function (feature, event) {
                        instance.options.clickHandler(event, feature);
                        instance.fire('lotclicked', {
                            event: event,
                            lot: feature,
                        });
                    },
                    filters: this.options.polygonInitialFilters,
                    scaleRange: [16, 18],
                    symbology: {
                        type: 'unique',
                        property: 'layer',
                        values: symbologyValues,
                    },
                    uniqueField: 'pk',
                    url: this.options.polygonBaseUrl,
                });
            },

            _loadPolygonLayer: function (queryString, clear) {
                if (!this.options.enablePolygons) return;
                if (!this.options.polygonBaseUrl) return;
                var instance = this;

                if (!instance.polygons) {
                    instance.polygons = instance._getPolygonLayer();
                }
                if (clear) {
                    //instance.clearPolygonLayer();
                }
                //instance.addLayer(instance.polygons);
                instance.polygons.setMap(instance);
            },


            /*
             * Centroids
             */

            _getCentroidLayer: function () {
                var instance = this;

                var symbologyValues = _.map(lotStyles, function (style, name) {
                    style.circleMarker = true;
                    return {
                        value: name,
                        vectorOptions: style
                    };
                });

                return new lvector.LotLayer({
                    map: null,
                    clickEvent: function (feature, event) {
                        instance.options.clickHandler(event, feature);
                        instance.fire('lotclicked', {
                            event: event,
                            lot: feature,
                        });
                    },
                    filters: instance.options.centroidInitialFilters,
                    scaleRange: [1, 16],
                    symbology: {
                        type: 'unique',
                        property: 'layer',
                        values: symbologyValues,
                    },
                    uniqueField: 'pk',
                    url: instance.options.centroidBaseUrl,
                });
            },

            _loadCentroidLayer: function (queryString) {
                if (!this.options.enableCentroids) return;
                if (!this.options.centroidBaseUrl) return;
                var instance = this;

                if (!instance.centroids) {
                    instance.centroids = instance._getCentroidLayer();
                }
            },

            addCentroidLayer: function (queryString) {
                this._loadCentroidLayer(queryString, true);
            },

            reloadCentroidLayer: function (filters) {
                if (this.centroids === undefined) return;
                this.centroids._clearFeatures();
                this.centroids._lastQueriedBounds = null;
                this.centroids.options.filters = filters;
                this.centroids._getFeatures();
            },

            showCentroidLayer: function () {
                var instance = this;
                instance.centroids.setMap(instance);
            },

            hideCentroidLayer: function () {
                var instance = this;
                if (instance.centroids) {
                    instance.centroids.setMap(null);
                }
            },


            /*
            * Choropleth
            */

            showChoropleth: function () {
                var instance = this;
                if (!instance.choropleth) {
                    instance.addChoroplethBoundaries(instance.filters['choropleth_boundary_layer']);
                }
                else {
                    instance.addLayer(instance.choropleth);
                }
            },

            hideChoropleth: function () {
                var instance = this;
                if (instance.choropleth) {
                    instance.removeLayer(instance.choropleth);
                }
            },

            reloadChoropleth: function (filters) {
                this.addChoroplethLayer(filters);
            },

            clearChoropleth: function () {
                var instance = this;
                instance.hideChoropleth();
                instance.choropleth = null;
                instance.choroplethLayers = {};
            },

            addChoroplethBoundaries: function (layer_name) {
                var instance = this;
                instance.choroplethBoundaryLayerName = layer_name;
                var url = Django.url('inplace:layer_view', { name: layer_name });
                instance.choroplethLayers = {};
                instance.fire('dataloading');
                $('#map').singleminded({
                    name: 'addChoroplethBoundaries',
                    jqxhr: $.getJSON(url, function (data) {
                        instance.choropleth = L.geoJson(data, {
                            onEachFeature: function (feature, layer) {
                                var boundaryLabel = feature.properties['boundary_label'];
                                instance.choroplethLayers[boundaryLabel] = layer;

                                layer.on({
                                    click: function () {
                                        // Zoom to this polygon? Maybe show other
                                        // details besides count (breakdown, area,
                                        // etc.)? TODO
                                    },
                                });
                            },
                        });
                        instance.updateChoroplethStyles(null);
                        if (instance.getZoom() < 16 && instance.viewType === 'choropleth') {
                            instance.choropleth.addTo(instance);
                        }

                        instance.updateChoropleth($.param(instance.filters, true));
                    })
                    .always(function () {
                        instance.fire('dataload');
                    }),
                });
            },

            getChoroplethColor: function (count, maxCount) {
                var instance = this;
                var hue = instance.choroplethHsl.hue,
                    saturation = instance.choroplethHsl.saturation,
                    lightness = instance.choroplethHsl.lightness;

                if (maxCount > 0) {
                    // Keep lightness between 30 and 90
                    lightness -= (count / maxCount) * 60;
                }
                return 'hsl(' + hue + ', ' + saturation + '%, ' + lightness + '%)';
            },

            getChoroplethStyle: function (count, maxCount) {
                var instance = this;
                var style = instance.choroplethStyle;
                style.fillColor = instance.getChoroplethColor(count, maxCount);
                return style;
            },

            updateChoroplethStyles: function (counts) {
                var instance = this;
                if (!instance.choroplethLayers) return;
                var maxCount = 0;

                if (counts && counts !== null) {
                    $.each(counts, function (layerLabel, count) {
                        maxCount = Math.max(maxCount, count);
                    });
                }

                $.each(instance.choroplethLayers, function (label, layer) {
                    var style = {};
                    if (counts && counts !== null) {
                        style = instance.getChoroplethStyle(counts[label], maxCount);
                    }
                    else {
                        style = instance.getChoroplethStyle(0, 0);
                    }
                    layer.setStyle(style);
                });

            },

            updateChoroplethLabels: function (counts) {
                var instance = this;

                $.each(counts, function (layerLabel, count) {
                    var layer = instance.choroplethLayers[layerLabel];
                    var label = layer._label;
                    var content = instance.choroplethBoundaryLayerName.slice(0, -1);
                    content += ' ' + layerLabel + '<br/ >' + count + ' lots';
                    if (label) {
                        layer.updateLabelContent(content);
                    }
                    else {
                        layer.bindLabel(content);
                    }
                });
            },

            addChoroplethLayer: function (filters) {
                var instance = this;
                if (!instance.options.enableChoropleth) return;

                var newLabel;
                var queryString = instance.options.choroplethQueryString;
                if (filters) {
                    newLabel = filters['choropleth_boundary_layer'];
                    queryString = $.param(filters, true);
                }

                // If boundaries don't yet exist or are new, load them
                if ((!instance.choropleth && newLabel) ||
                    (newLabel && newLabel !== instance.choroplethBoundaryLayerName)) {
                    instance.clearChoropleth();
                    instance.addChoroplethBoundaries(newLabel);
                }
                else {
                    instance.updateChoropleth(queryString);
                }
            },

            updateChoropleth: function (queryString) {
                var instance = this;

                // Update colors and labels
                var url = instance.options.choroplethBaseUrl + '?' + queryString;
                instance.fire('dataloading');
                $('#map').singleminded({
                    name: 'addChoroplethLayer',
                    jqxhr: $.getJSON(url, function (data) {
                        instance.updateChoroplethStyles(data);
                        instance.updateChoroplethLabels(data);
                    })
                    .always(function () {
                        instance.fire('dataload');
                    }),
                });

            },

            setVisibleLotsCount: function (count) {
                this.visibleLotsCount = count;
                this.pickChoroplethLayer();
            },

            /*
             * Determine the choropleth / summary view layer that should be
             * displayed. If it won't be too many lots, show centroids.
             */
            pickChoroplethLayer: function () {
                var instance = this;
                if (instance.viewType === 'choropleth') {
                    if (instance.visibleLotsCount <= instance.options.lotsCentroidThreshold) {
                        instance.hideChoropleth();
                        instance.showCentroidLayer();
                    }
                    else {
                        instance.hideCentroidLayer();
                        instance.showChoropleth();
                    }
                }
            },


            /*
            * Controls
            */

            addLayersControl: function () {
                if (!this.options.enableLayersControl) return;
                var baseLayers = {
                    'Streets': this.streets,
                    'Satellite': this.satellite,
                };
                var overlays = {};
                var layersControl = L.control.layers(baseLayers, overlays).addTo(this);
            },


            /*
            * Events
            */

            addZoomEvents: function () {
                var instance = this;
                instance.on('zoomend', function () {
                    var zoom = instance.getZoom();
                    if (zoom >= 16) {
                        instance.messageControl.hide();
                        instance.hideChoropleth();
                    }
                    else {
                        instance.messageControl.show();
                    }

                    if (zoom >= 17) {
                        instance.hideTiles();
                    }
                    else {
                        instance.showTiles();
                    }

                });
            },


            /*
            * Filters
            */

            updateFilters: function (filters) {
                this.filters = filters;

                // If the view type is changing, let the map know
                if (filters['view_type'] && filters['view_type'] !== this.viewType) {
                    this.changeView(filters['view_type']);
                }

                // Now, reload everything
                this.reloadCentroidLayer(filters);
                this.reloadChoropleth(filters);
                this.reloadPolygonLayer(filters);
                this.reloadTiles(filters);

                this.fire('moveend').fire('zoomend');
            },

            changeView: function (viewType) {
                this.viewType = viewType;
                this.fire('viewtypechange', { viewType: viewType });
                if (viewType === 'tiles') {
                    // Show tiles
                    this.showTiles();

                    // Hide everything else
                    this.hideChoropleth();
                }
                else if (viewType === 'choropleth') {
                    // Show choropleth
                    this.showChoropleth();

                    // Hide everything else
                    this.hideTiles();
                }
            },

        });

        L.Map.addInitHook('_lotMapInitialize');
    }
);
