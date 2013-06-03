define(
    [
        'jquery',
        'geocode',

        'jquery.plugin',
        'lib/jquery.spin',

    ], function ($, geocode) {
        var SearchBar = {

            init: function (options, elem) {
                var instance = this;
                instance.options = $.extend({}, instance.options, options);
                instance.elem = elem;
                instance.$elem = $(elem);

                instance.$elem.keypress(function (e) {
                    if (e.keyCode === '13') {
                        e.preventDefault();
                        instance.searchByAddress();
                        return false;
                    }
                });
                instance.$elem.find('form').submit(function (e) {
                    e.preventDefault();
                    instance.searchByAddress();
                    return false;
                });
            },


            options: {
                bounds: null,
                city: null,
                state: null,
                errorMessage: null,
                warningSelector: null,
            },

            addCityAndState: function (query) {
                var city = this.options.city.toLowerCase();
                if (query.toLowerCase().indexOf(city) <= 0) {
                    query += ', ' + city;
                }

                var state = this.options.state.toLowerCase();
                if (query.toLowerCase().indexOf(state) <= 0) {
                    query += ', ' + state;
                }
                return query;
            },

            searchByAddress: function () {
                var instance = this;
                instance.$elem.find(instance.options.warningSelector).hide();
                instance.$elem.find(':input[type=submit]')
                    .spin('small')
                    .attr('disabled', 'disabled');

                var query = instance.$elem.find('input[type="text"]').val();
                query = instance.addCityAndState(query);

                geocode(query, instance.options.bounds, instance.options.state, function (result, status) {
                    // Done searching
                    instance.$elem.find(':input[type=submit]')
                        .spin(false)
                        .removeAttr('disabled');

                    // Is result valid?
                    if (result === null) {
                        instance.$elem.find(instance.options.warningSelector)
                            .text(instance.options.errorMessage)
                            .show();
                        return;
                    }

                    // Let the world know!
                    var found_location = result.geometry.location;
                    instance.$elem.trigger('searchresultfound', [{
                        longitude: found_location.lng(),
                        latitude: found_location.lat(),
                        query_address: query,
                        found_address: result.formatted_address,
                    }]);
                });
            },

        };

        $.plugin('searchbar', SearchBar);
    }
);
