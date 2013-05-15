//
// A very simple AJAX requests queue of length 1.
//
// For requests that will be made repeatedly and that only the most recent 
// should be adhered to.
//
define(['jquery', 'jquery.plugin',], function($) {
    var SingleMinded = {

        init: function(options, elem) {
            var instance = this;
            instance.options = $.extend({}, instance.options, options);
            instance.elem = elem;
            instance.$elem = $(elem);

            if (!instance.$elem.data('thoughts')) {
                instance.$elem.data('thoughts', {});
            }
            instance.remember(instance.options.name, instance.options.jqxhr);
        },

        forget: function(name) {
            var instance = this;
            var request = instance.$elem.data('thoughts')[name];

            // If request exists and does not have a DONE state, abort it
            if (request && request.readyState != 4) {
                request.abort();
            }

            instance.$elem.data('thoughts')[name] = null;
        },

        remember: function(name, jqxhr) {
            var instance = this;
            instance.forget(name);

            jqxhr.done(function() {
                // Don't bother remembering requests we've finished
                instance.forget(name);
            });
            instance.$elem.data('thoughts')[name] = jqxhr;
        },

    };

    $.plugin('singleminded', SingleMinded);
});
