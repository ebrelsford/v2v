import os

from .base import *

ADMINS = (
    ('Eric', 'ebrelsford@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = [get_env_variable('PHILLY_ALLOWED_HOSTS')]

#
# johnny cache
#
MIDDLEWARE_CLASSES = (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
) + MIDDLEWARE_CLASSES

CACHES = {
    'default' : dict(
        BACKEND = 'johnny.backends.memcached.MemcachedCache',
        LOCATION = [get_env_variable('PHILLY_MEMCACHE_LOCATION')],
        JOHNNY_CACHE = True,
    )
}

JOHNNY_MIDDLEWARE_KEY_PREFIX = get_env_variable('PHILLY_CACHE_KEY_PREFIX')


#
# email
#
INSTALLED_APPS += (
    'mailer',
)
EMAIL_BACKEND = 'mailer.backend.DbBackend'
EMAIL_HOST = get_env_variable('PHILLY_EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('PHILLY_EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('PHILLY_EMAIL_PASSWORD')
EMAIL_PREFIX = '[Grounded 215] '
DEFAULT_FROM_EMAIL = get_env_variable('PHILLY_DEFAULT_FROM_EMAIL')
SERVER_EMAIL = get_env_variable('PHILLY_SERVER_EMAIL')


#
# logging
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'log_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'logs', 'django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['log_file', 'mail_admins'],
        'level': 'WARNING',
    },
}

LOT_SURVEY_FORM_PK = 1

LOT_MAP_TILE_URLS = {
    'private': 'http://tiles.v2v.webfactional.com/lot_points_private/',
    'private_grid': 'http://tiles.v2v.webfactional.com/lot_points_private_grid/',
    'public': 'http://tiles.v2v.webfactional.com/lot_points_public/',
    'public_grid': 'http://tiles.v2v.webfactional.com/lot_points_public_grid/',
}
