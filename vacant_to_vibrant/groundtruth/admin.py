from django.contrib import admin

from django_monitor.admin import MonitorAdmin

from .models import GroundtruthRecord


class GroundtruthRecordAdmin(MonitorAdmin):
    list_display = ('pk', 'use', 'contact_email', 'contact_phone', 'added',)


admin.site.register(GroundtruthRecord, GroundtruthRecordAdmin)
