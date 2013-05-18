from django.conf import settings


def map_tile_urls(request):
    return {
        'lot_tile_urls': settings.LOT_MAP_TILE_URLS,
    }
