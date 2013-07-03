from django.contrib import admin

from admin_enhancer.admin import EnhancedModelAdminMixin
from django_monitor.admin import MonitorAdmin

from .models import StewardNotification, StewardProject


class StewardNotificationAdmin(EnhancedModelAdminMixin, MonitorAdmin):
    fields = ('stewarded_target', 'name', 'use', 'support_organization',
              'land_tenure_status', 'include_on_map', 'phone', 'email', 'type',
              'url', 'facebook_page',)
    list_display = ('pk', 'name', 'stewarded_target',)
    readonly_fields = ('content_type', 'object_id', 'stewarded_target',)

    def stewarded_target(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                obj.content_object.get_absolute_url(),
                obj.content_object
            )
        except Exception:
            return ''
    stewarded_target.allow_tags = True


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
