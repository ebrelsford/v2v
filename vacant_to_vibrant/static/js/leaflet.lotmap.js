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
        lotTilesBaseUrl: String,
        lotGridBaseUrl: String,
        lotCentroidBaseUrl: String,
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

        // Add controls
        this.addLayersControl();
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

});

L.Map.addInitHook('_lotMapInitialize');
