var StreetView = {

    init: function(options, elem) {
        this.options = $.extend({}, this.options, options);

        this.elem = elem;
        this.$elem = $(elem);

        this.load_streetview();
        this.service = new google.maps.StreetViewService();

        return this;
    },

    options: {
        errorSelector: '#streetview-error',
    },

    load_streetview: function(lon, lat) {
        var instance = this;
        instance.$elem.hide();
        $(instance.options.errorSelector).hide();

        if (!(lon && lat)) return;
        var latLng = new google.maps.LatLng(lat, lon);

        instance.service.getPanoramaByLocation(latLng, 50, function(result, status) {
            if (status == google.maps.StreetViewStatus.OK) {
                instance.$elem.show();
                new google.maps.StreetViewPanorama(instance.elem, {
                    pano: result.location.pano,
                });
            }
            else {
                $(instance.options.errorSelector).show();
            }
        });
    },

};

$.plugin('streetview', StreetView);
