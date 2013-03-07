from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from reversion_compare.admin import CompareVersionAdmin

from .models import LandUseArea


class LandUseAreaAdmin(OSMGeoAdmin, CompareVersionAdmin):
    date_hierarchy = 'added'
    list_display = ('object_id', 'category', 'subcategory', 'description',
                    'added', 'area',)
    list_filter = ('category', 'subcategory',)
    search_fields = ('description',)

admin.site.register(LandUseArea, LandUseAreaAdmin)
