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

        // Leaflet plugins
        'lib/leaflet.label',
        'lib/leaflet.utfgrid',
        'Leaflet.Bing',
        'leaflet.geojsonbounds',
        'leaflet.lotlayer',
        'leaflet.message',

        // Other plugins
        'jquery.singleminded',

    ], function($, L, lvector, Django) {

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

        choroplethBoundaryLayerName: null,
        filters: {},
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

        addPointPrivateTilesLayer: function() {
            if (!(this.options.enablePointPrivateTiles && this.viewType === 'tiles')) return;
            if (!this.options.pointPrivateTilesBaseUrl) return;

            var url = this.options.pointPrivateTilesBaseUrl + '{z}/{x}/{y}.png';
            this.tilesPointPrivate = L.tileLayer(url).addTo(this);
        },

        addPointPrivateGridLayer: function() {
            if (!(this.options.enablePointPrivateTiles && this.viewType === 'tiles')) return;
            if (!this.options.pointPrivateGridBaseUrl) return;
            var url = this.options.pointPrivateGridBaseUrl 
                + '{z}/{x}/{y}.json?callback={cb}';
            this.gridPointPrivate = new L.UtfGrid(url, {
                resolution: this.options.gridResolution,
            });
            if (this.options.clickHandler) {
                var map = this;
                map.gridPointPrivate.on('click', function(e) {
                    e.targetType = 'utfgrid';
                    map.options.clickHandler(e);
                });
            }
            this.addLayer(this.gridPointPrivate);
        },

        addPointPublicTilesLayer: function() {
            if (!(this.options.enablePointPublicTiles && this.viewType === 'tiles')) return;
            if (!this.options.pointPublicTilesBaseUrl) return;

            var url = this.options.pointPublicTilesBaseUrl + '{z}/{x}/{y}.png';
            this.tilesPointPublic = L.tileLayer(url).addTo(this);
        },

        addPointPublicGridLayer: function() {
            if (!(this.options.enablePointPublicTiles && this.viewType === 'tiles')) return;
            if (!this.options.pointPublicGridBaseUrl) return;
            var url = this.options.pointPublicGridBaseUrl 
                + '{z}/{x}/{y}.json?callback={cb}';
            this.gridPointPublic = new L.UtfGrid(url, {
                resolution: this.options.gridResolution,
            });
            if (this.options.clickHandler) {
                var map = this;
                map.gridPointPublic.on('click', function(e) {
                    e.targetType = 'utfgrid';
                    map.options.clickHandler(e);
                });
            }
            this.addLayer(this.gridPointPublic);
        },

        showTiles: function() {
            this.addLayer(this.tilesPointPublic);
            this.addLayer(this.gridPointPublic);
            this.addLayer(this.tilesPointPrivate);
            this.addLayer(this.gridPointPrivate);
        },

        hideTiles: function() {
            var instance = this;
            instance.removeLayer(instance.tilesPointPublic);
            instance.removeLayer(instance.gridPointPublic);
            instance.removeLayer(instance.tilesPointPrivate);
            instance.removeLayer(instance.gridPointPrivate);
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
            if (instance.choroplethLabels) {
                $.each(instance.choroplethLabels, function(i, label) {
                    label.addTo(instance);
                });
            }

            if (!instance.choropleth) {
                instance.addChoroplethBoundaries(instance.filters.boundary_layer);
            }
            else {
                instance.addLayer(instance.choropleth);
            }
        },

        hideChoropleth: function() {
            var instance = this;
            if (instance.choroplethLabels) {
                $.each(instance.choroplethLabels, function(i, label) {
                    instance.removeLayer(label);
                });
            }
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
            instance.choroplethLabels = {};
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
                            instance.choroplethLayers[feature.properties.boundary_label] = layer;
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
            if (!instance.choroplethLayers) return;
            if (instance.choroplethLabels === undefined) {
                instance.choroplethLabels = {};
            }

            $.each(counts, function(layerLabel, count) {
                var layer = instance.choroplethLayers[layerLabel];
                var label = instance.choroplethLabels[layerLabel] || new L.Label();
                // TODO dynamic by layer name
                label.setContent('Council District ' + layerLabel + '<br/ >' 
                    + count + ' lots');
                label.setLatLng(layer.getBounds().getCenter());
                instance.choroplethLabels[layerLabel] = label;

                if (instance.viewType === 'choropleth') {
                    instance.showLabel(label);
                }
            });
        },

        addChoroplethLayer: function(filters) {
            var instance = this;
            if (!instance.options.enableChoropleth) return;

            var newLabel;
            var queryString = instance.options.choroplethQueryString;
            if (filters) {
                newLabel = filters.boundary_layer;
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
                    if (instance.viewType === 'tiles') {
                        instance.showTiles();
                    }
                }

            });
        },


        /*
         * Filters
         */

        updateFilters: function(filters) {
            // If the view type is changing, let the map know
            if (filters.view_type && filters.view_type !== this.viewType) {
                this.viewType = filters.view_type;
                this.changeView(this.viewType);
            }
            this.filters = filters;

            // Now, reload everything
            this.reloadChoropleth(filters);
            this.reloadPolygonLayer(filters);

            this.fire('moveend').fire('zoomend');
        },

        changeView: function(viewType) {
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
