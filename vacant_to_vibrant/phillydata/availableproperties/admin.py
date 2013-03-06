from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from reversion_compare.admin import CompareVersionAdmin

from .models import AvailableProperty


class AvailablePropertyAdmin(OSMGeoAdmin, CompareVersionAdmin):
    date_hierarchy = 'last_seen'
    list_display = ('address', 'price_str', 'area', 'status', 'last_seen',)
    list_filter = ('status', 'agency',)
    search_fields = ('address', 'description',)

admin.site.register(AvailableProperty, AvailablePropertyAdmin)
