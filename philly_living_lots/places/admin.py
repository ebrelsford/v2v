from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin


class PlaceAdmin(OSMGeoAdmin, admin.ModelAdmin):
    list_display = ('name', 'city', 'state_province',)

    @staticmethod
    def get_address_fieldset():
        return ('Address', {
            'fields': (
                ('address_line1', 'address_line2', 'postal_code',),
                ('city', 'state_province', 'country',),
            ),
        })

    @staticmethod
    def get_geo_fieldset():
        return ('Geo', {
            'fields': (
                'centroid',
                'polygon',
            ),
        })
