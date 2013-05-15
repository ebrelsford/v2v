/*
 * L.LotMap -- mixin for L.Map that adds layers for vacant to vibrant.
 */

define(
    [
        // Dependencies we'll use the return values from
        'jquery',
        'leaflet',
        'lib/leaflet.lvector',

        // Leaflet plugins
        'lib/leaflet.label',
        'lib/leaflet.lvector',
        'Leaflet.Bing',
        'leaflet.geojsonbounds',
        'leaflet.lotlayer',
        'leaflet.message',

        // Other plugins
        'jquery.singleminded',

    ], function($, L, lvector) {

    L.Map.include({

        /*
        options: {
            bingKey: String,
            cloudmadeKey: String,
            cloudmadeStyleId: String,
            enableLayersControl: Boolean,
            enableLotChoropleth: Boolean,
            enableLotPolygons: Boolean,
            lotTilesBaseUrl: String,
            lotGridBaseUrl: String,
            lotCentroidBaseUrl: String,
            lotPolygonBaseUrl: String,
            lotPolygonInitialFilters: Object,
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

        _lotMapInitialize: function() {
            this._initLayers();

            // Add base layers
            this.addSatelliteLayer(false);
            this.addStreetsLayer();

            // Add overlays
            this.addLotTilesLayer();
            this.addLotGridLayer();
            this.addLotCentroidLayer();
            this.addLotChoroplethLayer();
            this.addLotPolygonLayer();

            // Add controls
            this.addLayersControl();

            // Add events
            this.addZoomEvents();
        },

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

        addLotTilesLayer: function() {
            if (!this.options.lotTilesBaseUrl) return;
            var url = this.options.lotTilesBaseUrl + '{z}/{x}/{y}.png';
            this.lots = L.tileLayer(url).addTo(this);
        },

        addLotGridLayer: function() {
            if (!this.options.lotGridBaseUrl) return;
            var url = this.options.lotGridBaseUrl + '{z}/{x}/{y}.json?callback={cb}';
            this.lotsUtfgrid = new L.UtfGrid(url, {
                resolution: this.options.lotGridResolution,
            });
            if (this.options.lotClickHandler) {
                var map = this;
                map.lotsUtfgrid.on('click', function(e) {
                    e.targetType = 'utfgrid';
                    map.options.lotClickHandler(e);
                });
            }
            this.addLayer(this.lotsUtfgrid);
        },

        _getLotCentroidLayer: function() {
            return new L.MarkerClusterGroup({
                getGeoJsonFromData: function(data) {
                    return data.objects;
                },
                getNextPageUrlFromData: function(data) {
                    return data.meta.next;
                },
            });
        },

        _loadLotCentroidLayer: function(queryString, clear) {
            if (!this.options.lotCentroidBaseUrl) return;
            var map = this;

            if (!map.lotsCentroids) {
                map.lotsCentroids = map._getLotCentroidLayer();
            }
            if (clear) {
                map.clearLotCentroidLayer();
            }

            var url = this.options.lotCentroidBaseUrl + '?' + queryString;
            map.lotsCentroids.addPaginatedLayer(url, {
                onEachFeature: function(feature, layer) {
                    if (!map.options.lotClickHandler) return;
                    layer.on('click', function(e) {
                        e.data = feature;
                        e.targetType = 'layer';
                        map.options.lotClickHandler(e);
                        map.fire('lotclicked', feature);
                    });
                },   
            });
            map.addLayer(map.lotsCentroids);
        },

        _getLotPolygonLayer: function() {
            var instance = this;
            return new lvector.LotLayer({
                clickEvent: function(feature, event) {
                    instance.options.lotClickHandler(event, feature);
                    instance.fire('lotclicked', {
                        event: event,
                        lot: feature,
                    });
                },
                filters: this.options.lotPolygonInitialFilters,
                scaleRange: [15, 18],
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
                url: this.options.lotPolygonBaseUrl,
            });
        },

        _loadLotPolygonLayer: function(queryString, clear) {
            if (!this.options.enableLotPolygons) return;
            if (!this.options.lotPolygonBaseUrl) return;
            var map = this;

            if (!map.lotPolygons) {
                map.lotPolygons = map._getLotPolygonLayer();
            }
            if (clear) {
                //map.clearLotPolygonLayer();
            }
            //map.addLayer(map.lotPolygons);
            map.lotPolygons.setMap(map);
        },

        clearLotCentroidLayer: function() {
            if (this.lotsCentroids) {
                this.lotsCentroids.clearLayers();
            }
            else {
                this.lotsCentroids = new L.MarkerClusterGroup();
            }
        },

        addLotCentroidLayer: function(queryString) {
            if (!queryString) {
                queryString = this.options.lotCentroidQueryString;
            }
            this._loadLotCentroidLayer(queryString, true);
        },

        addToLotCentroidLayer: function(queryString) {
            this._loadLotCentroidLayer(queryString, false);
        },

        reloadLotCentroidLayer: function(queryString) {
            this._loadLotCentroidLayer(queryString, true);
        },

        updateFilters: function(filters) {
            if (this.lotPolygons === undefined) return;
            this.lotPolygons._clearFeatures();
            this.lotPolygons._lastQueriedBounds = null;

            this.lotPolygons.options.filters = filters;
            this.lotPolygons._getFeatures();
            this.fire('moveend').fire('zoomend');
        },

        addLotPolygonLayer: function(queryString) {
            if (!queryString) {
                queryString = this.options.lotPolygonQueryString;
            }
            this._loadLotPolygonLayer(queryString, true);
        },

        addToLotPolygonLayer: function(queryString) {
            this._loadLotPolygonLayer(queryString, false);
        },

        reloadLotPolygonLayer: function(queryString) {
            this._loadLotPolygonLayer(queryString, true);
        },

        addLayersControl: function() {
            if (!this.options.enableLayersControl) return;
            var baseLayers = {
                'Streets': this.streets, 
                'Satellte': this.satellite, 
            };
            if (this.lotsUtfgrid && this.lots) {
                var overlays = {
                    'lots': L.layerGroup([this.lots, this.lotsUtfgrid]),
                };
            }
            var layersControl = L.control.layers(baseLayers, overlays).addTo(this);
        },

        reloadLotChoroplethLayer: function(queryString) {
            this.addLotChoroplethLayer(queryString);
        },

        addLotChoroplethBoundaries: function(layer_name) {
            var instance = this;
            // TODO in a setting through data attributes
            var url = '/places/boundaries/layers/' + layer_name + '/';
            instance.lotsChoroplethLayers = {};
            $('#map').singleminded({
                name: 'addLotChoroplethBoundaries',
                jqxhr: $.getJSON(url, function(data) {
                    instance.lotsChoropleth = L.geoJson(data, {
                        onEachFeature: function(feature, layer) {
                            instance.lotsChoroplethLayers[feature.properties.boundary_label] = layer;
                        },
                    });
                    instance.updateLotChoroplethStyles(null);
                    if (instance.getZoom() < 15) {
                        instance.lotsChoropleth.addTo(instance);
                    }
                }),
            });
        },

        getLotChoroplethColor: function(count, maxCount) {
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

        getLotChoroplethStyle: function(count, maxCount) {
            var instance = this;
            var style = instance.choroplethStyle;
            style.fillColor = instance.getLotChoroplethColor(count, maxCount);
            return style;
        },

        updateLotChoroplethStyles: function(counts) {
            var instance = this;
            var maxCount = 0;

            if (counts && counts !== null) {
                $.each(counts, function(layerLabel, count) {
                    maxCount = Math.max(maxCount, count);
                });
            }

            $.each(instance.lotsChoroplethLayers, function(label, layer) {
                var style = {};
                if (counts && counts !== null) {
                    style = instance.getLotChoroplethStyle(counts[label], maxCount);
                }
                else {
                    style = instance.getLotChoroplethStyle(0, 0);
                }
                layer.setStyle(style);
            });

            /*
            $.each(counts, function(layerLabel, count) {
                var style = instance.getLotChoroplethStyle(count, maxCount);
                instance.lotsChoroplethLayers[layerLabel].setStyle(style);
            });
            */
        },

        updateLotChoroplethLabels: function(counts) {
            var instance = this;
            if (instance.lotsChoroplethLabels === undefined) {
                instance.lotsChoroplethLabels = {};
            }

            $.each(counts, function(layerLabel, count) {
                var layer = instance.lotsChoroplethLayers[layerLabel];
                var label = instance.lotsChoroplethLabels[layerLabel] || new L.Label();
                label.setContent('Council District ' + layerLabel + '<br/ >' 
                    + count + ' lots');
                label.setLatLng(layer.getBounds().getCenter());
                instance.lotsChoroplethLabels[layerLabel] = label;
                instance.showLabel(label);
            });
        },

        addLotChoroplethLayer: function(queryString) {
            var instance = this;
            if (!instance.options.enableLotChoropleth) return;
            if (!queryString) queryString = instance.options.lotChoroplethQueryString;

            // If boundaries don't yet exist, load them
            if (instance.lotsChoropleth === undefined) {
                instance.addLotChoroplethBoundaries('City Council Districts');
            }

            // Update colors and labels
            var url = instance.options.lotChoroplethBaseUrl + '?' + queryString;
            $('#map').singleminded({
                name: 'addLotChoroplethLayer',
                jqxhr: $.getJSON(url, function(data) {
                    instance.updateLotChoroplethStyles(data);
                    instance.updateLotChoroplethLabels(data);
                }),
            });
        },

        addZoomEvents: function() {
            var instance = this;
            instance.on('zoomend', function() {
                var zoom = instance.getZoom();
                if (zoom >= 15) {
                    // Hide choropleth
                    if (instance.lotsChoropleth) {
                        // Hide labels
                        $.each(instance.lotsChoroplethLabels, function(i, label) {
                            instance.removeLayer(label);
                        });

                        // Hide message
                        if (instance.messageControl._map) {
                            instance.messageControl.removeFrom(instance);
                        }

                        instance.removeLayer(instance.lotsChoropleth);
                    }
                    // Polygon visibility is controlled by vector layers
                }
                else {
                    // Show choropleth
                    if (instance.lotsChoropleth) {
                        // Show labels
                        if (instance.lotsChoroplethLabels) {
                            $.each(instance.lotsChoroplethLabels, function(i, label) {
                                label.addTo(instance);
                            });
                        }
                        // Show message
                        if (!instance.messageControl._map) {
                            instance.messageControl.addTo(instance);
                        }

                        instance.addLayer(instance.lotsChoropleth);
                    }
                }
            });
        },

    });

    L.Map.addInitHook('_lotMapInitialize');
});
