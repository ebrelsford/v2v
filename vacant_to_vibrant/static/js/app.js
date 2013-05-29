requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'django': 'djangojs/django',
        'jquery': 'lib/jquery-1.10.0.min',
        'jquery.infinitescroll': 'lib/jquery.infinitescroll.min',
        'fancybox': 'lib/fancybox/jquery.fancybox.pack',
        'leaflet': 'lib/leaflet',
        'underscore': 'lib/underscore-min',
        'async': 'lib/async',
        'json2': 'lib/json2',
        'spin': 'lib/spin.min',
    },
    shim: {
        'django': {
            'deps': ['jquery'],
            'exports': 'Django',
        },
        'leaflet': {
            exports: 'L',
        },
        'underscore': {
            exports: '_',
        },
        'json2': {
            exports: 'JSON',
        },
        'lib/leaflet.lvector': {
            deps: ['leaflet'],
            exports: 'lvector',
        },
        'Leaflet.Bing': ['leaflet'],
        'lib/leaflet.label': ['leaflet'],
        'lib/leaflet.utfgrid': ['leaflet'],
        'chosen.jquery.min': ['jquery'],
        'chosen.jquery_ready': ['jquery', 'chosen.jquery.min'],
    },
});

// Load the main app module to start the app
requirejs(['main']);
