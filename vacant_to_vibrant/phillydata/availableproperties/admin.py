from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from reversion_compare.admin import CompareVersionAdmin

from .models import AvailableProperty


class AvailablePropertyAdmin(OSMGeoAdmin, CompareVersionAdmin):
    date_hierarchy = 'last_seen'
    list_display = ('address', 'price_str', 'area', 'status', 'last_seen',
                    'has_lot',)
    list_filter = ('status', 'agency',)
    search_fields = ('address', 'description',)

    def has_lot(self, obj):
        count = obj.lot_set.all().count()
        if count == 0:
            return 'no'
        if count == 1:
            return 'yes'
        if count > 1:
            return 'many'

admin.site.register(AvailableProperty, AvailablePropertyAdmin)
