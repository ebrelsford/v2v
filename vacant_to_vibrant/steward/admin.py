from django.contrib import admin
from django.core.urlresolvers import reverse

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
              'land_tenure_status', 'include_on_map', 'share_contact_details',
              'phone', 'email', 'type',
              'url', 'facebook_page',)
    list_display = ('pk', 'name', 'stewarded_target',)
    readonly_fields = ('content_type', 'object_id', 'stewarded_target',)


class StewardProjectAdmin(BaseStewardAdminMixin, admin.ModelAdmin):

    fields = ('stewarded_target', 'name', 'use', 'support_organization',
              'land_tenure_status', 'include_on_map', 'organizer',
              'date_started', 'external_id', 'pilcop_garden_id',
              'steward_notification_link',)
    list_display = ('pk', 'pilcop_garden_id', 'name', 'stewarded_target',
                    'organizer', 'use', 'include_on_map',)
    list_filter = ('use', 'include_on_map',)
    readonly_fields = ('content_type', 'object_id', 'stewarded_target',
                       'steward_notification_link',)
    search_fields = ('name', 'pilcop_garden_id',)

    def steward_notification_link(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                reverse('admin:steward_stewardnotification_change',
                        args=(obj.steward_notification.pk,)),
                obj.steward_notification,
            )
        except Exception:
            return '(none)'
    steward_notification_link.allow_tags = True


admin.site.register(StewardNotification, StewardNotificationAdmin)
admin.site.register(StewardProject, StewardProjectAdmin)
