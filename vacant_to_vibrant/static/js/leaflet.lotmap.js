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
    },
    */

    _lotMapInitialize: function() {
        this._initLayers();
        this.addBaseLayer();
        this.addSatelliteLayer();
        this.addLotTilesLayer();
        this.addLotGridLayer();

        this.addLayersControl();
        this.addClickHandler();
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
        this.addLayer(this.lotsUtfgrid);
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

    addClickHandler: function() {
        if (!this.options.lotClickHandler) return;

        if (this.lotsUtfgrid) {
            this.lotsUtfgrid.on('click', this.options.lotClickHandler);
        }
        
        // add other potential lot layers here
    },

});

L.Map.addInitHook('_lotMapInitialize');
