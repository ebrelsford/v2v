from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Parcel


class ParcelAdmin(OSMGeoAdmin, admin.ModelAdmin):
    list_display = ('basereg', 'address',)

admin.site.register(Parcel, ParcelAdmin)
