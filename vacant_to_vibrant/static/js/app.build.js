({

    baseUrl: '.',
    //appDir: '.',
    //dir: '../built',

    mainConfigFile: 'app.js',

    name: 'lib/almond',
    out: '../main-built.js',
    include: [

        // Main module
        'main',

        // Per-page modules
        'lotbasepage',
        'addorganizerpage',
        'mappage',
        'mailparticipantspage',

        // require()d dependencies
        'chosen.jquery_ready',
        'fancybox',
        'lib/jquery.noisy'
    ],
    insertRequire: ['main'],

    // Let django-compressor take care of CSS
    optimizeCss: "none",
    optimize: "uglify2",

    preserveLicenseComments: true,
    
})
