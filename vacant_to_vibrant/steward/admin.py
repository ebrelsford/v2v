from django.contrib import admin

from admin_enhancer.admin import EnhancedModelAdminMixin
from django_monitor.admin import MonitorAdmin

from .models import StewardNotification, StewardProject


class BaseStewardAdminMixin(EnhancedModelAdminMixin):

    def stewarded_target(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                obj.content_object.get_absolute_url(),
                obj.content_object
            )
        except Exception:
            return ''
    stewarded_target.allow_tags = True


class StewardNotificationAdmin(BaseStewardAdminMixin, MonitorAdmin):

    fields = ('stewarded_target', 'name', 'use', 'support_organization',
              'land_tenure_status', 'include_on_map', 'phone', 'email', 'type',
              'url', 'facebook_page',)
    list_display = ('pk', 'name', 'stewarded_target',)
    readonly_fields = ('content_type', 'object_id', 'stewarded_target',)


class StewardProjectAdmin(BaseStewardAdminMixin, admin.ModelAdmin):

    fields = ('stewarded_target', 'name', 'use', 'support_organization',
              'land_tenure_status', 'include_on_map', 'organizer',
              'date_started', 'external_id',)
    list_display = ('pk', 'name', 'stewarded_target', 'organizer', 'use',
                    'include_on_map',)
    list_filter = ('use', 'include_on_map',)
    readonly_fields = ('content_type', 'object_id', 'stewarded_target',)


admin.site.register(StewardNotification, StewardNotificationAdmin)
admin.site.register(StewardProject, StewardProjectAdmin)
