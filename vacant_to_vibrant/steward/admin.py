from django.contrib import admin

from admin_enhancer.admin import EnhancedModelAdminMixin
from django_monitor.admin import MonitorAdmin

from .models import StewardNotification, StewardProject


class StewardNotificationAdmin(EnhancedModelAdminMixin, MonitorAdmin):
    list_display = ('pk', 'name',)


class StewardProjectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'address', 'organizer', 'use',
                    'include_on_map',)
    list_filter = ('use', 'include_on_map',)

    def address(self, obj):
        try:
            return obj.content_object.address_line1
        except Exception:
            return ''


admin.site.register(StewardNotification, StewardNotificationAdmin)
admin.site.register(StewardProject, StewardProjectAdmin)
