/*
 * Extend Leaflet Vector Layer's GeoJSONLayer to intelligently display polygons
 * and centroids of lots.
 */

define(
    [
        'leaflet',
        'lib/leaflet.lvector',
        'json2',

    ], function (L, lvector, JSON) {

        lvector.LotLayer = lvector.GeoJSONLayer.extend({

            initialize: function (options) {
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
                        this.options.visibleAtScale = (z >= sr[0] && z <= sr[1]);
                    }
                    this._show();
                }
            },

            options: {
                filters: {},
                url: null,
            },

            // Override zoom change listener--only check visibility if the 
            // layer is on a map currently.
            _zoomChangeListenerTemplate: function () {
                var instance = this;
                return function () {
                    if (instance.getMap()) {
                        instance._checkLayerVisibility();
                    }
                };
            },

            _requiredParams: ["url",],

            _getFeatures: function () {
                // Only load when map at a visible zoom
                if (!this.options.visibleAtScale || !this.getMap()) {
                    return;
                }

                // Add bounds to filters
                this.options.filters.centroid__within = JSON.stringify(
                        this.getMap().getBounds().toGeoJson());

                // Build request url
                var url = this.options.url + '?' + $.param(this.options.filters, true);
                this._makeJsonRequest(url, this._processFeatures);
            },

            _makeJsonRequest: function (url, callback) {
                var instance = this;
                instance.getMap().fire('dataloading');
                $.getJSON(url, function (data) {
                    // Ensure this is the layer
                    callback.apply(instance, [data,]);
                })
                .always(function () {
                    if (instance.getMap()) {
                        instance.getMap().fire('dataload');
                    }
                });
            },

        });
    }
);
