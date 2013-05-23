define(['leaflet'], function(L) {
    L.Control.Message = L.Control.extend({
        options: {
            defaultHtml: 'Message goes here.',
            position: 'topcenter',
        },

        initialize: function(options) {
            L.setOptions(this, options);
        },

        onAdd: function(map) {
            this._container = L.DomUtil.create('div', 'leaflet-control-message');
            L.DomEvent.disableClickPropagation(this._container);

            this._update(this.options.defaultHtml);

            return this._container;
        },

        hide: function() {
            L.DomUtil.addClass(this._container, 'is-hidden');
        },

        show: function() {
            L.DomUtil.removeClass(this._container, 'is-hidden');
        },

        setMessage: function(html) {
            this._update(html);
        },

        _update: function (html) {
            if (!this._map) { return; }
            this._container.innerHTML = html;
        },

    });

    L.Map.addInitHook(function () {
        if (!this.options.messageControl) { return; }
        var className = 'leaflet-top leaflet-center';
        this._controlCorners['topcenter'] = 
            L.DomUtil.create('div', className, this._controlContainer);
        this.messageControl = (new L.Control.Message({
            defaultHtml: this.options.messageDefault,
        })).addTo(this);
    });

    L.control.message = function(options) {
        return new L.Control.Message(options);
    };
});
