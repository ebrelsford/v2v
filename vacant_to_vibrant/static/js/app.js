requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'django': 'djangojs/django',
        'jquery': 'lib/jquery-1.10.2.min',
        'jqueryui': 'lib/jquery-ui-1.10.3.custom',
        'jquery.infinitescroll': 'lib/jquery.infinitescroll.min',
        'fancybox': 'lib/fancybox/jquery.fancybox.pack',
        'leaflet': 'lib/leaflet',
        'underscore': 'lib/underscore-min',
        'async': 'lib/async',
        'json2': 'lib/json2',
        'spin': 'lib/spin.min',
        'leaflet.usermarker': 'lib/leaflet.usermarker/leaflet.usermarker',
    },
    shim: {
        'django': {
            'deps': ['jquery'],
            'exports': 'Django',
        },
        'underscore': {
            exports: '_',
        },
        'bootstrap': {
            deps: ['jquery'],
        },
        'json2': {
            exports: 'JSON',
        },
        'lib/leaflet.lvector': {
            deps: ['leaflet'],
            exports: 'lvector',
        },
        'Control.Loading': ['leaflet'],
        'Leaflet.Bing': ['leaflet'],
        'lib/leaflet.label': ['leaflet'],
        'lib/leaflet.utfgrid': ['leaflet'],
        'leaflet.usermarker': ['leaflet'],
        'chosen.jquery.min': ['jquery'],
        'chosen.jquery_ready': ['jquery', 'chosen.jquery.min'],
        'lib/jquery.noisy': ['jquery'],
        'lib/bootstrap/bootstrap-dropdown': ['jquery'],
        'lib/bootstrap/bootstrap-tooltip': ['jquery'],
    },
});

// Load the main app module to start the app
requirejs(['main']);
