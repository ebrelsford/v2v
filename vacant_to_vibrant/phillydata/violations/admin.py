from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Violation, ViolationLocation, ViolationType


class ViolationAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'violation_datetime',)
    readonly_fields = ('violation_location', 'violation_type',)
    search_fields = ('violation_location__address',)


class ViolationLocationAdmin(OSMGeoAdmin, admin.ModelAdmin):
    list_display = ('address', 'zip_code', 'external_id',)
    search_fields = ('address', 'zip_code', 'external_id',)


class ViolationTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'li_description',)


admin.site.register(Violation, ViolationAdmin)
admin.site.register(ViolationLocation, ViolationLocationAdmin)
admin.site.register(ViolationType, ViolationTypeAdmin)
