from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Violation, ViolationLocation, ViolationType


class ViolationAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'violation_datetime',)


class ViolationLocationAdmin(OSMGeoAdmin, admin.ModelAdmin):
    list_display = ('address', 'zip_code', 'external_id',)


class ViolationTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'li_description',)


admin.site.register(Violation, ViolationAdmin)
admin.site.register(ViolationLocation, ViolationLocationAdmin)
admin.site.register(ViolationType, ViolationTypeAdmin)
