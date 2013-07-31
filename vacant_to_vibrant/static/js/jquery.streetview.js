define(['jquery', 'jquery.plugin',], function ($) {
    var StreetView = {

        init: function (options, elem) {
            this.options = $.extend({}, this.options, options);

            this.elem = elem;
            this.$elem = $(elem);

            this.service = new google.maps.StreetViewService();

            return this;
        },

        options: {
            errorSelector: '#streetview-error',
        },

        get_heading: function (lon0, lat0, lon1, lat1) {
            // Don't bother with great-circle calculations--should be close!
            var r = Math.atan2(-(lon1 - lon0), (lat1 - lat0));
            if (r < 0) {
                r += 2 * Math.PI;
            }
            var d = r * (180 / Math.PI);

            // Convert to google's heading: "True north is 0°, east is 90°,
            // south is 180°, west is 270°."
            if (d >= 45 && d < 135) { d += 180; }
            else if (d >= 225 && d < 315) { d -= 180; }
            return d;
        },

        load_streetview: function (lon, lat) {
            var instance = this;
            instance.$elem.hide();
            $(instance.options.errorSelector).hide();

            if (!(lon && lat)) return;
            var latLng = new google.maps.LatLng(lat, lon);

            instance.service.getPanoramaByLocation(latLng, 50, function (result, status) {
                // TODO result.imageDate could be useful

                if (status === google.maps.StreetViewStatus.OK) {
                    instance.$elem.show();
                    var lon0 = result.location.latLng.lng(),
                        lat0 = result.location.latLng.lat();

                    new google.maps.StreetViewPanorama(instance.elem, {
                        pano: result.location.pano,
                        pov: {
                            heading: instance.get_heading(lon0, lat0, lon, lat),
                            pitch: 0,
                        },
                    });
                }
                else {
                    $(instance.options.errorSelector).show();
                }
            });
        },

    };

    $.plugin('streetview', StreetView);
});
