from django.contrib import admin

from django_monitor.admin import MonitorAdmin

from .models import GroundtruthRecord


class GroundtruthRecordAdmin(MonitorAdmin):
    list_display = ('pk', 'use', 'address', 'contact_name', 'contact_email',
                    'contact_phone', 'added',)

    def address(self, obj):
        try:
            return obj.content_object.address_line1
        except Exception:
            return ''


admin.site.register(GroundtruthRecord, GroundtruthRecordAdmin)
