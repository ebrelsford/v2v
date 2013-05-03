/*
 * L.LotMap -- mixin for L.Map that adds layers for vacant to vibrant.
 */

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

    clearLotChoroplethLayer: function() {
        var instance = this;
        if (instance.lotsChoropleth) {
            instance.lotsChoropleth.clearLayers();
        }
        if (instance.lotsChoroplethLabels) {
            // TODO actually destroy each label?
            $.each(instance.lotsChoroplethLabels, function(i, label) {
                label.close();
            });
            instance.lotsChoroplethLabels = [];
        }
    },

    addLotChoroplethLayer: function(queryString) {
        var instance = this;
        if (!instance.options.enableLotChoropleth) return;
        if (!queryString) queryString = instance.options.lotChoroplethQueryString;

        // TODO instead of clearing the layer, update colors and labels?
        // could be smoother
        instance.clearLotChoroplethLayer();

        var url = instance.options.lotChoroplethBaseUrl + '?' + queryString;
        $('#map').singleminded({
            name: 'lotChoroplethRequest',
            jqxhr: $.getJSON(url, function(data) {

                var _getColor = function(count) {
                    // TODO make dynamic base on count range
                    //  Use colorbrewer: colorbrewer2.org
                    var color = 
                        count > 5000 ? '#238443' :
                        count > 1000 ? '#78C679' :
                        count > 100 ? '#C2E699' :
                            '#FFFFCC';
                    return color;
                };

                instance.lotsChoroplethLabels = [];
                instance.lotsChoropleth = L.geoJson(data, {
                    style: function(feature) {
                        return {
                            fillColor: _getColor(feature.properties.count),
                            fillOpacity: .7,
                            color: 'white',
                            opacity: .8,
                            weight: 2,
                        };
                    },   

                    onEachFeature: function(feature, layer) {
                        label = new L.Label();
                        label.setContent('City Council District ' + feature.properties.boundary_label + '<br/ >' +
                            feature.properties.count);

                        // TODO we might want to set centroids manually for weirder
                        // polygons like city council districts

                        label.setLatLng(layer.getBounds().getCenter());
                        instance.lotsChoroplethLabels.push(label);
                        instance.showLabel(label);
                    },
                });
                if (instance.getZoom() < 15) {
                    instance.lotsChoropleth.addTo(instance);
                }
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
                    $.each(instance.lotsChoroplethLabels, function(i, label) {
                        label.addTo(instance);
                    });
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
