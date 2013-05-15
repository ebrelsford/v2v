define(['leaflet'], function(L) {
    L.extend(L.LatLngBounds.prototype, {

        fromGeoJson: function(geoJson) {
            var ne = geoJson.coordinates[0][2],
                sw = geoJson.coordinates[0][0];

            // Construct LatLngBounds, swapping x,y to get lat,lng
            return L.latLngBounds([
                [ne[1], ne[0]],
                [sw[1], sw[0]]
            ]);
        },

        toGeoJson: function() {
            return {
                'type': 'Polygon',
                'coordinates': [[
                    [this.getSouthWest().lng, this.getSouthWest().lat],
                    [this.getNorthWest().lng, this.getNorthWest().lat],
                    [this.getNorthEast().lng, this.getNorthEast().lat],
                    [this.getSouthEast().lng, this.getSouthEast().lat],
                    [this.getSouthWest().lng, this.getSouthWest().lat],
                ]],
            }
        },

    });


    /*
     * Shortcut for creating LatLngBounds out of a GeoJSON string representing the
     * bounding box to be converted to LatLngBounds.
     */
    L.geoJsonLatLngBounds = function(geoJsonString) {
        var geoJson = JSON.parse(geoJsonString);
        return L.LatLngBounds.prototype.fromGeoJson(geoJson);
    };
});
