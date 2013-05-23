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

        // Leaflet plugins
        'lib/leaflet.label',
        'lib/leaflet.utfgrid',
        'Leaflet.Bing',
        'leaflet.geojsonbounds',
        'leaflet.lotlayer',
        'leaflet.message',

        // Other plugins
        'jquery.singleminded',

    ], function($, L, lvector, Django, _) {

    L.Map.include({

        /*
        options: {
            bingKey: String,
            cloudmadeKey: String,
            cloudmadeStyleId: String,
            enableLayersControl: Boolean,
            enableChoropleth: Boolean,
            enablePointTiles: Boolean,
            enablePolygons: Boolean,
            polygonBaseUrl: String,
            polygonInitialFilters: Object,
            messageControl: Boolean,
            messageDefault: String,
        },
        */

        choroplethHsl: {
            hue: 140,
            saturation: 42,
            lightness: 90,
        },

        choroplethStyle: {
            fillOpacity: .7,
            color: 'white',
            opacity: .8,
            weight: 2,
        },

        tileLayers: {
            'public': [],
            'private': [],
        },

        choroplethBoundaryLayerName: null,
        filters: {},
        ownerTypes: ['private', 'public'],
        viewType: 'tiles',


        _lotMapInitialize: function() {
            this._initLayers();

            // Add base layers
            this.addSatelliteLayer(false);
            this.addStreetsLayer();

            // Add overlays
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

        addStreetsLayer: function() {
            this.streets = L.tileLayer(
                'http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', 
                {
                    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://www.openstreetmap.org/copyright">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
                    key: this.options.cloudmadeKey,
                    styleId: this.options.cloudmadeStyleId,
                }
            ).addTo(this);
        },

        addSatelliteLayer: function(add) {
            this.satellite = new L.BingLayer(this.options.bingKey)
            if (add) this.satellite.addTo(this);
        },


        /*
         * Overlay layers
         */


        /*
         * Tiles layers
         */

        addTilesLayers: function() {
            this.addPointPrivateTilesLayer();
            this.addPointPrivateGridLayer();
            this.addPointPublicTilesLayer();
            this.addPointPublicGridLayer();
        },

        addGridLayer: function(baseUrl) {
            if (!baseUrl) return;
            var instance = this;
            var url = baseUrl + '{z}/{x}/{y}.json?callback={cb}';
            var gridLayer = new L.UtfGrid(url, {
                resolution: this.options.gridResolution,
            });
            if (instance.options.clickHandler) {
                gridLayer.on('click', function(e) {
                    e.targetType = 'utfgrid';
                    instance.options.clickHandler(e);
                });
            }
            instance.addLayer(gridLayer);
            return gridLayer;
        },

        addPointPrivateTilesLayer: function() {
            if (!(this.options.enablePointPrivateTiles && this.viewType === 'tiles')) return;
            if (!this.options.pointPrivateTilesBaseUrl) return;

            var url = this.options.pointPrivateTilesBaseUrl + '{z}/{x}/{y}.png';
            this.tilesPointPrivate = L.tileLayer(url).addTo(this);
            this.tileLayers['private'].push(this.tilesPointPrivate);
        },

        addPointPrivateGridLayer: function() {
            if (!(this.options.enablePointPrivateTiles && this.viewType === 'tiles')) return;
            this.gridPointPrivate = this.addGridLayer(this.options.pointPrivateGridBaseUrl);
            this.tileLayers['private'].push(this.gridPointPrivate);
        },

        addPointPublicTilesLayer: function() {
            if (!(this.options.enablePointPublicTiles && this.viewType === 'tiles')) return;
            if (!this.options.pointPublicTilesBaseUrl) return;

            var url = this.options.pointPublicTilesBaseUrl + '{z}/{x}/{y}.png';
            this.tilesPointPublic = L.tileLayer(url).addTo(this);
            this.tileLayers['public'].push(this.tilesPointPublic);
        },

        addPointPublicGridLayer: function() {
            if (!(this.options.enablePointPublicTiles && this.viewType === 'tiles')) return;
            this.gridPointPublic = this.addGridLayer(this.options.pointPublicGridBaseUrl);
            this.tileLayers['public'].push(this.gridPointPublic);
        },

        showTiles: function() {
            var instance = this;
            if (instance.viewType !== 'tiles') return;
            var filtered = _.size(instance.filters) > 0;
            var activeOwnerTypes = instance.getActiveOwnerTypes(instance.filters);

            _.each(instance.ownerTypes, function(ownerType) {
                if (!filtered) {
                    // Always show if there are no current filters
                    instance.showOwnerTypeTiles(ownerType);
                }
                else if (activeOwnerTypes.indexOf(ownerType) >= 0) {
                    instance.showOwnerTypeTiles(ownerType);
                }
                else {
                    instance.hideOwnerTypeTiles(ownerType);
                }
            });
        },

        hideTiles: function() {
            var instance = this;
            _.each(instance.ownerTypes, function(ownerType) {
                instance.hideOwnerTypeTiles(ownerType);
            });
        },

        showOwnerTypeTiles: function(ownerType) {
            var instance = this;
            _.each(instance.tileLayers[ownerType], function(layer) {
                if (layer) {
                    instance.addLayer(layer);
                }
            });
        },

        hideOwnerTypeTiles: function(ownerType) {
            var instance = this;
            _.each(instance.tileLayers[ownerType], function(layer) {
                if (layer) {
                    instance.removeLayer(layer);
                }
            });
        },

        getActiveOwnerTypes: function(filters) {
            var activeOwnerTypes = filters['owner__owner_type__in'];
            if (!activeOwnerTypes) {
                return [];
            }
            else if (!_.isArray(activeOwnerTypes)) {
                return [activeOwnerTypes,];
            }
            return activeOwnerTypes;
        },

        /*
         * Update which tiles are shown by owner type
         */
        reloadTiles: function(filters) {
            var instance = this;
            instance.filters = filters;
            instance.showTiles();
        },


        /*
         * Polygons
         */

        addPolygonLayer: function(queryString) {
            if (!queryString) {
                queryString = this.options.polygonQueryString;
            }
            this._loadPolygonLayer(queryString, true);
        },

        addToPolygonLayer: function(queryString) {
            this._loadPolygonLayer(queryString, false);
        },

        reloadPolygonLayer: function(filters) {
            if (this.polygons === undefined) return;
            this.polygons._clearFeatures();
            this.polygons._lastQueriedBounds = null;
            this.polygons.options.filters = filters;
            this.polygons._getFeatures();
        },

        _getPolygonLayer: function() {
            var instance = this;
            return new lvector.LotLayer({
                clickEvent: function(feature, event) {
                    instance.options.clickHandler(event, feature);
                    instance.fire('lotclicked', {
                        event: event,
                        lot: feature,
                    });
                },
                filters: this.options.polygonInitialFilters,
                scaleRange: [16, 18],
                symbology: {
                    type: 'single',
                    vectorOptions: {
                        fillColor: '#78C679',
                        fillOpacity: .7,
                        color: 'white',
                        opacity: .8,
                        weight: 1,
                    },
                },
                uniqueField: 'pk',
                url: this.options.polygonBaseUrl,
            });
        },

        _loadPolygonLayer: function(queryString, clear) {
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
         * Choropleth
         */

        showChoropleth: function() {
            var instance = this;
            if (!instance.choropleth) {
                instance.addChoroplethBoundaries(instance.filters['boundary_layer']);
            }
            else {
                instance.addLayer(instance.choropleth);
            }
        },

        hideChoropleth: function() {
            var instance = this;
            if (instance.choropleth) {
                instance.removeLayer(instance.choropleth);
            }
        },

        reloadChoropleth: function(filters) {
            this.addChoroplethLayer(filters);
        },

        clearChoropleth: function() {
            var instance = this;
            instance.hideChoropleth();
            instance.choropleth = null;
            instance.choroplethLayers = {};
        },

        addChoroplethBoundaries: function(layer_name) {
            var instance = this;
            instance.choroplethBoundaryLayerName = layer_name;
            var url = Django.url('inplace:layer_view', { name: layer_name });
            instance.choroplethLayers = {};
            $('#map').singleminded({
                name: 'addChoroplethBoundaries',
                jqxhr: $.getJSON(url, function(data) {
                    instance.choropleth = L.geoJson(data, {
                        onEachFeature: function(feature, layer) {
                            var boundaryLabel = feature.properties['boundary_label'];
                            instance.choroplethLayers[boundaryLabel] = layer;

                            layer.on({
                                click: function() {
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

                    instance.updateChoropleth($.param(instance.filters));
                }),
            });
        },

        getChoroplethColor: function(count, maxCount) {
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

        getChoroplethStyle: function(count, maxCount) {
            var instance = this;
            var style = instance.choroplethStyle;
            style.fillColor = instance.getChoroplethColor(count, maxCount);
            return style;
        },

        updateChoroplethStyles: function(counts) {
            var instance = this;
            if (!instance.choroplethLayers) return;
            var maxCount = 0;

            if (counts && counts !== null) {
                $.each(counts, function(layerLabel, count) {
                    maxCount = Math.max(maxCount, count);
                });
            }

            $.each(instance.choroplethLayers, function(label, layer) {
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

        updateChoroplethLabels: function(counts) {
            var instance = this;

            $.each(counts, function(layerLabel, count) {
                var layer = instance.choroplethLayers[layerLabel];
                var label = layer._label;
                // TODO dynamic by layer name OR when we get counts?
                var content = 'Council District ' + layerLabel + '<br/ >' + count + ' lots';
                if (label) {
                    layer.updateLabelContent(content);
                }
                else {
                    layer.bindLabel(content);
                }
            });
        },

        addChoroplethLayer: function(filters) {
            var instance = this;
            if (!instance.options.enableChoropleth) return;

            var newLabel;
            var queryString = instance.options.choroplethQueryString;
            if (filters) {
                newLabel = filters['boundary_layer'];
                queryString = $.param(filters);
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

        updateChoropleth: function(queryString) {
            var instance = this;

            // Update colors and labels
            var url = instance.options.choroplethBaseUrl + '?' + queryString;
            $('#map').singleminded({
                name: 'addChoroplethLayer',
                jqxhr: $.getJSON(url, function(data) {
                    instance.updateChoroplethStyles(data);
                    instance.updateChoroplethLabels(data);
                }),
            });

        },


        /*
         * Controls
         */

        addLayersControl: function() {
            if (!this.options.enableLayersControl) return;
            var baseLayers = {
                'Streets': this.streets, 
                'Satellte': this.satellite, 
            };
            var overlays = {};
            if (this.options.enablePointPrivateTiles) {
                overlays['Lot Points (private)'] = L.layerGroup([
                        this.tilesPointPrivate, this.gridPointPrivate]);
            }
            if (this.options.enablePointPublicTiles) {
                overlays['Lot Points (public)'] = L.layerGroup([
                        this.tilesPointPublic, this.gridPointPublic]);
            }
            var layersControl = L.control.layers(baseLayers, overlays).addTo(this);
        },


        /*
         * Events
         */

        addZoomEvents: function() {
            var instance = this;
            instance.on('zoomend', function() {
                var zoom = instance.getZoom();
                if (zoom >= 16) {
                    // Hide choropleth
                    if (instance.choropleth) {
                        instance.hideChoropleth();
                    }
                    // Polygon visibility is controlled by vector layers

                }
                else {
                    if (instance.viewType === 'choropleth') {
                        instance.showChoropleth();
                    }
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

        updateFilters: function(filters) {
            this.filters = filters;

            // If the view type is changing, let the map know
            if (filters['view_type'] && filters['view_type'] !== this.viewType) {
                this.changeView(filters['view_type']);
            }

            // Now, reload everything
            this.reloadChoropleth(filters);
            this.reloadPolygonLayer(filters);
            this.reloadTiles(filters);

            this.fire('moveend').fire('zoomend');
        },

        changeView: function(viewType) {
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
});
