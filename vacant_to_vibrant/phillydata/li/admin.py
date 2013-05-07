from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Location


class LocationAdmin(OSMGeoAdmin, admin.ModelAdmin):
    list_display = ('address', 'zip_code', 'external_id',)
    search_fields = ('address', 'zip_code', 'external_id',)

admin.site.register(Location, LocationAdmin)
