
L.extend(L.LatLngBounds.prototype, {

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
