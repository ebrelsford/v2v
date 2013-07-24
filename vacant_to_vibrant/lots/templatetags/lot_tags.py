import json

from django import template


register = template.Library()


def main_map_url(lot):
    default_filters = ('parents_only=True&known_use_existence=not+in+use&'
                       'known_use_existence=in+use&'
                       'available_property__status__in=new+and+available&'
                       'available_property__status__in=available&'
                       'view_type=tiles&owner__owner_type__in=mixed&'
                       'owner__owner_type__in=private&'
                       'owner__owner_type__in=public')
    centroid = json.dumps({
        'lat': lot.centroid.y,
        'lng': lot.centroid.x,
    })
    return '/?%s&centroid=%s&zoom=18' % (default_filters, centroid)

register.filter('main_map_url', main_map_url)
