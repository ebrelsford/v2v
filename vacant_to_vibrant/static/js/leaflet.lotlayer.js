/*
 * Extend Leaflet Vector Layer's GeoJSONLayer to intelligently display polygons
 * of lots.
 */

define(
    [
        'leaflet',
        'lib/leaflet.lvector',
        'json2',

    ], function(L, lvector, JSON) {

    lvector.LotLayer = lvector.GeoJSONLayer.extend({

        initialize: function(options) {
            // Check for required parameters
            for (var i = 0, len = this._requiredParams.length; i < len; i++) {
                if (!options[this._requiredParams[i]]) {
                    throw new Error("No \"" + this._requiredParams[i] +
                        "\" parameter found.");
                }
            }

            // Extend Layer
            lvector.Layer.prototype.initialize.call(this, options);

            // Create an array to hold the features
            this._vectors = [];

            if (this.options.map) {
                if (this.options.scaleRange && this.options.scaleRange instanceof Array && this.options.scaleRange.length === 2) {
                    var z = this.options.map.getZoom();
                    var sr = this.options.scaleRange;
                    // TODO make sure features being loaded when zoom changes get
                    // hidden if they are fully loaded after zooming and we are out
                    // of range

                    // TODO make sure these generally do not load if the zoom is
                    // wrong
                    this.options.visibleAtScale = (z >= sr[0] && z <= sr[1]);
                }
                this._show();
            }
        },

        options: {
            filters: {},
            url: null,
        },

        _requiredParams: ["url",],

        _getFeatures: function() {        
            // Only load when map at a visible zoom
            if (!this.options.visibleAtScale) {
                return;
            }

            // Add bounds to filters
            this.options.filters.centroid__within = JSON.stringify(
                    this.getMap().getBounds().toGeoJson());

            // Build request url
            var url = this.options.url + '?' + $.param(this.options.filters, true);
            this._makeJsonRequest(url, this._processFeatures);
        },

        _makeJsonRequest: function(url, callback) {
            var instance = this;
            this.getMap().fire('dataloading');
            $.getJSON(url, function(data) {
                // Ensure this is the layer
                callback.apply(instance, [data,]);
            })
            .always(function() {
                this.getMap().fire('dataload');
            });
        },

    });
});
