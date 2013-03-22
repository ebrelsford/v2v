from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Lot


class LotAdmin(OSMGeoAdmin, admin.ModelAdmin):
    exclude = ('centroid',)
    list_display = ('address_line1', 'city', 'owner', 'billing_account',)
    readonly_fields = ('land_use_area', 'parcel', 'violations',)

admin.site.register(Lot, LotAdmin)
