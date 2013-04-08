/*
 * A mixin for MarkerClusterGroup that adds paginated layers. In the options
 * for the MarkerClusterGroup, two functions should be added:
 *
 *  // get the GeoJSON collection from the data
 *  getGeoJsonFromData: function(data) {}
 *
 *  // get the next page url from the data
 *  getNextPageUrlFromData: function(data) {}
 *
 *
 * TODO: A way to stop loading pages before they have all loaded.
 *
 */
L.MarkerClusterGroup.include({

    addPaginatedLayer: function(url, geoJsonOptions) {
        this.addDataByUrl(url, geoJsonOptions, true);
    },

    addDataByUrl: function(url, geoJsonOptions, paginated) {
        var instance = this;
        $.getJSON(url, function(data) {

            // Add the data we fetched
            var layer = L.geoJson(
                instance.options.getGeoJsonFromData(data),
                geoJsonOptions
            );
            instance.addLayer(layer);

            // Can we get more data?
            if (!paginated) return;
            var next_url = instance.options.getNextPageUrlFromData(data);
            if (!next_url) return;

            // XXX stop-gap, would need a more robust solution if we planned on
            // using this
            if ($('#stop-loading:checked').length > 0) return;

            // Get more data!
            instance.addDataByUrl(next_url, geoJsonOptions, paginated);
        });
    },

});
