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
        lotCentroidUrl: String,
    },
    */

    _lotMapInitialize: function() {
        this._initLayers();
        this.addBaseLayer();
        this.addSatelliteLayer();
        this.addLotTilesLayer();
        this.addLotGridLayer();
        this.addLotCentroidLayer();

        this.addLayersControl();
    },

    addBaseLayer: function() {
        this.streets = L.tileLayer(
            'http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', 
            {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://www.openstreetmap.org/copyright">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
                key: this.options.cloudmadeKey,
                styleId: this.options.cloudmadeStyleId,
            }
        ).addTo(this);
    },

    addSatelliteLayer: function() {
        this.satellite = new L.BingLayer(this.options.bingKey)
            .addTo(this);
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

    addLotCentroidLayer: function() {
        if (!this.options.lotCentroidUrl) return;
        var map = this;
        $.getJSON(this.options.lotCentroidUrl, function(data) {
            var geojsonLayer = L.geoJson(data, {
                onEachFeature: function(feature, layer) {
                    if (!map.options.lotClickHandler) return;
                    layer.on('click', function(e) {
                        e.data = feature;
                        e.targetType = 'layer';
                        map.options.lotClickHandler(e);
                    });
                },   
            });
            var markerCluster = new L.MarkerClusterGroup();
            markerCluster.addLayer(geojsonLayer);
            map.addLayer(markerCluster);
        });
    },

    addLayersControl: function() {
        if (!this.options.enableLayersControl) return;
        var interactiveLayerGroup = L.layerGroup([this.lots, this.lotsUtfgrid]);
        var layersControl = L.control.layers(
            { 
                'Satellte': this.satellite, 
                'Streets': this.streets, 
            }, 
            { 
                'lots': interactiveLayerGroup,
            }
        ).addTo(this);
    },

});

L.Map.addInitHook('_lotMapInitialize');
