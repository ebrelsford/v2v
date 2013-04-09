from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import BaseDistrict, ZoningType


class BaseDistrictAdmin(OSMGeoAdmin):
    list_display = ('id', 'zoning_type',)
    list_filter = ('zoning_type',)
    fieldsets = (
        (None, {
            'fields': ('zoning_type', 'geometry',),
        }),
    )


class ZoningTypeAdmin(OSMGeoAdmin):
    list_display = ('code', 'long_code', 'group',)
    list_filter = ('group', 'code',)
    search_fields = ('code', 'long_code', 'group',)

admin.site.register(BaseDistrict, BaseDistrictAdmin)
admin.site.register(ZoningType, ZoningTypeAdmin)
