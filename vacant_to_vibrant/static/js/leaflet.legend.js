define(['leaflet'], function(L) {
    L.Control.Legend = L.Control.extend({
        options: {
            featureTypes: [],
            position: 'bottomleft',
        },

        initialize: function (options) {
            L.setOptions(this, options);
        },

        onAdd: function (map) {
            this._container = L.DomUtil.create('div', 'leaflet-control-legend');
            L.DomEvent.disableClickPropagation(this._container);

            this.legendFeatures = L.DomUtil.create('ul', 'leaflet-control-legend-features', this._container);
            this._update(this.options.featureTypes);

            return this._container;
        },

        hide: function () {
            L.DomUtil.addClass(this._container, 'is-hidden');
        },

        show: function () {
            L.DomUtil.removeClass(this._container, 'is-hidden');
        },

        setFeatureTypes: function (featureTypes) {
            this._update(featureTypes);
        },

        _slugify: function (s) {
            return s.replace(' ', '-');
        },

        _update: function (featureTypes) {
            if (!this._map) { return; }
            var classes = 'leaflet-control-legend-feature-color leaflet-control-legend-feature-color-';
            for (var i = 0; i < featureTypes.length; i++) {
                var featureItem = L.DomUtil.create('li', 'leaflet-control-legend-feature', this.legendFeatures);
                L.DomUtil.create('span',  classes + this._slugify(featureTypes[i].name), featureItem);
                var label = L.DomUtil.create('label', '', featureItem);
                label.innerHTML = featureTypes[i].name;
            }
        },

    });

    L.control.legend = function (options) {
        return new L.Control.Legend(options);
    };

    L.Map.addInitHook(function () {
        if (!this.options.legendControl) { return; }
        var className = 'leaflet-bottom leaflet-left';
        this.legendControl = L.control.legend({
            featureTypes: this.options.legendFeatureTypes,
        }).addTo(this);
    });
});
