({

    baseUrl: '.',
    //appDir: '.',
    //dir: '../built',

    mainConfigFile: 'app.js',

    name: 'lib/almond',
    out: '../main-built.js',
    include: [
        'main',
        'lotbasepage',
        'addorganizerpage',
        'mappage',
        'mailparticipantspage',
        'chosen.jquery_ready'
    ],
    insertRequire: ['main'],

    // Let django-compressor take care of CSS
    optimizeCss: "none",
    optimize: "uglify2",

    preserveLicenseComments: true,
    
})
