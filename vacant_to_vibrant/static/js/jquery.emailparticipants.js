define(
    [
        // Dependencies we'll use the return values from
        'jquery',
        'django',

        'jquery.plugin',

        'lib/jquery.form',
        'lib/jquery.spin',

    ], function($, Django) {
    var EmailParticipants = {

        options: {
            filterContainer: null,
        },

        init: function(options, elem) {
            var instance = this;
            instance.options = $.extend({}, instance.options, options);
            instance.elem = elem;
            instance.$elem = $(elem);

            // Add our container
            instance.$container = $('<div></div>').addClass('email-participants-container');
            instance.$elem.after(instance.$container);

            instance.options.filterContainer.on('filterschange', function(e) {
                instance._updateFilters(e.filters);
                instance._updateCounts();
            });

            // Show form on click
            instance.$elem.click(function() {
                if (!instance.$container.is(':visible')) {
                    instance.show();
                }
                else {
                    instance.hide();
                }
                return false;
            });
        },

        show: function() {
            var instance = this;

            instance.$container.spin('small');
            instance.$container
                .show()
                .load(Django.url('extraadmin:mail_participants'), function() {
                    instance.$container.spin(false);
                    instance._initializeForm();
                    instance._updateCounts();
                });
        },

        hide: function() {
            var instance = this;
            instance.$container.hide();
        },

        _initializeForm: function() {
            var instance = this;
            instance._updateCounts();
            instance.$container.find('form')
                .ajaxForm({
                    target: instance.$container,
                    success: function() {
                        // Initialize again in case the form was sent back due 
                        // to validation
                        instance._initializeForm();
                        instance.$container.spin(false);
                    },
                })
                .submit(function() {
                    instance.$container.spin('small');
                });
        },

        _updateCounts: function() {
            var instance = this;
            if (!instance.filters) return;
            var url = Django.url('extraadmin:mail_participants_count')
                + '?' + $.param(instance.filters, true);
            $.getJSON(url, function(data) {
                instance.$container.find('.organizer-count').text(data.organizers);
                instance.$container.find('.watcher-count').text(data.watchers);
            });
        },

        _updateFilters: function(filters) {
            var instance = this;
            instance.filters = filters;

            var $form = instance.$container.find('form');
            if ($form.length === 0) return;
            $form.find(':input[name=filters]').val($.param(filters, true));
        },

    };

    $.plugin('emailparticipants', EmailParticipants);
});
